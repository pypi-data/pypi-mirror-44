#
# Copyright (c) 2017 Intel Corporation
# SPDX-License-Identifier: BSD-2-Clause
#

from __future__ import print_function, division, absolute_import
import types as pytypes  # avoid confusion with numba.types
import numpy
import operator
from numba import ir, analysis, types, config, cgutils, typing
from numba.ir_utils import (
    mk_unique_var,
    replace_vars_inner,
    find_topo_order,
    dprint_func_ir,
    get_global_func_typ,
    guard,
    require,
    get_definition,
    find_callname,
    find_build_sequence,
    find_const,
    is_namedtuple_class)
from numba.analysis import (compute_cfg_from_blocks)
from numba.typing import npydecl, signature
import collections
import copy
from numba.extending import intrinsic
import llvmlite.llvmpy.core as lc
import llvmlite

UNKNOWN_CLASS = -1
CONST_CLASS = 0
MAP_TYPES = [numpy.ufunc]

array_analysis_extensions = {}

# declaring call classes
array_creation = ['empty', 'zeros', 'ones', 'full']

random_int_args = ['rand', 'randn']

random_1arg_size = ['ranf', 'random_sample', 'sample',
                    'random', 'standard_normal']

random_2arg_sizelast = ['chisquare', 'weibull', 'power',
                        'geometric', 'exponential',
                        'poisson', 'rayleigh']

random_3arg_sizelast = ['normal', 'uniform', 'beta',
                        'binomial', 'f', 'gamma',
                        'lognormal', 'laplace']

random_calls = (random_int_args +
                random_1arg_size +
                random_2arg_sizelast +
                random_3arg_sizelast +
                ['randint', 'triangular'])

@intrinsic
def wrap_index(typingctx, idx, size):
    """
    Calculate index value "idx" relative to a size "size" value as
    (idx % size), where "size" is known to be positive.
    Note that we use the mod(%) operation here instead of
    (idx < 0 ? idx + size : idx) because we may have situations
    where idx > size due to the way indices are calculated
    during slice/range analysis.
    """
    if idx != size:
        raise ValueError("Argument types for wrap_index must match")

    def codegen(context, builder, sig, args):
        assert(len(args) == 2)
        idx = args[0]
        size = args[1]
        rem = builder.srem(idx, size)
        zero = llvmlite.ir.Constant(idx.type, 0)
        is_negative = builder.icmp_signed('<', rem, zero)
        wrapped_rem = builder.add(rem, size)
        is_oversize = builder.icmp_signed('>', wrapped_rem, size)
        mod = builder.select(is_negative, wrapped_rem,
                builder.select(is_oversize, rem, wrapped_rem))
        return mod

    return signature(idx, idx, size), codegen

@intrinsic
def assert_equiv(typingctx, *val):
    """
    A function that asserts the inputs are of equivalent size,
    and throws runtime error when they are not. The input is
    a vararg that contains an error message, followed by a set
    of objects of either array, tuple or integer.
    """
    if len(val) > 1:
        # Make sure argument is a single tuple type. Note that this only
        # happens when IR containing assert_equiv call is being compiled
        # (and going through type inference) again.
        val = (types.Tuple(val),)

    assert(len(val[0]) > 1)
    # Arguments must be either array, tuple, or integer
    assert all(map(lambda a: (isinstance(a, types.ArrayCompatible) or
                              isinstance(a, types.BaseTuple) or
                              isinstance(a, types.SliceType) or
                              isinstance(a, types.Integer)), val[0][1:]))

    def codegen(context, builder, sig, args):
        assert(len(args) == 1)  # it is a vararg tuple
        tup = cgutils.unpack_tuple(builder, args[0])
        tup_type = sig.args[0]
        msg = sig.args[0][0].literal_value

        def unpack_shapes(a, aty):
            if isinstance(aty, types.ArrayCompatible):
                ary = context.make_array(aty)(context, builder, a)
                return cgutils.unpack_tuple(builder, ary.shape)
            elif isinstance(aty, types.BaseTuple):
                return cgutils.unpack_tuple(builder, a)
            else:  # otherwise it is a single integer
                return [a]

        def pairwise(a, aty, b, bty):
            ashapes = unpack_shapes(a, aty)
            bshapes = unpack_shapes(b, bty)
            assert len(ashapes) == len(bshapes)
            for (m, n) in zip(ashapes, bshapes):
                m_eq_n = builder.icmp(lc.ICMP_EQ, m, n)
                with builder.if_else(m_eq_n) as (then, orelse):
                    with then:
                        pass
                    with orelse:
                        context.call_conv.return_user_exc(
                            builder, AssertionError, (msg,))

        for i in range(1, len(tup_type) - 1):
            pairwise(tup[i], tup_type[i], tup[i + 1], tup_type[i + 1])
        r = context.get_constant_generic(builder, types.NoneType, None)
        return r
    return signature(types.none, *val), codegen


class EquivSet(object):

    """EquivSet keeps track of equivalence relations between
    a set of objects.
    """

    def __init__(self, obj_to_ind=None, ind_to_obj=None, next_ind=0):
        """Create a new EquivSet object. Optional keyword arguments are for
        internal use only.
        """
        # obj_to_ind maps object to equivalence index (sometimes also called
        # equivalence class) is a non-nagative number that uniquely identifies
        # a set of objects that are equivalent.
        self.obj_to_ind = obj_to_ind if obj_to_ind else {}
        # ind_to_obj maps equivalence index to a list of objects.
        self.ind_to_obj = ind_to_obj if ind_to_obj else {}
        # next index number that is incremented each time a new equivalence
        # relation is created.
        self.next_ind = next_ind

    def empty(self):
        """Return an empty EquivSet object.
        """
        return EquivSet()

    def clone(self):
        """Return a new copy.
        """
        return EquivSet(obj_to_ind=copy.deepcopy(self.obj_to_ind),
                        ind_to_obj=copy.deepcopy(self.ind_to_obj),
                        next_id=self.next_ind)

    def __repr__(self):
        return "EquivSet({})".format(self.ind_to_obj)

    def is_empty(self):
        """Return true if the set is empty, or false otherwise.
        """
        return self.obj_to_ind == {}

    def _get_ind(self, x):
        """Return the internal index (greater or equal to 0) of the given
        object, or -1 if not found.
        """
        return self.obj_to_ind.get(x, -1)

    def _get_or_add_ind(self, x):
        """Return the internal index (greater or equal to 0) of the given
        object, or create a new one if not found.
        """
        if x in self.obj_to_ind:
            i = self.obj_to_ind[x]
        else:
            i = self.next_ind
            self.next_ind += 1
        return i

    def _insert(self, objs):
        """Base method that inserts a set of equivalent objects by modifying
        self.
        """
        assert len(objs) > 1

        inds = tuple(self._get_or_add_ind(x) for x in objs)
        ind = min(inds)

        if not (ind in self.ind_to_obj):
            self.ind_to_obj[ind] = []

        for i, obj in zip(inds, objs):
            if i == ind:
                if not (obj in self.ind_to_obj[ind]):
                    self.ind_to_obj[ind].append(obj)
                    self.obj_to_ind[obj] = ind
            else:
                if i in self.ind_to_obj:
                    # those already existing are reassigned
                    for x in self.ind_to_obj[i]:
                        self.obj_to_ind[x] = ind
                        self.ind_to_obj[ind].append(x)
                    del self.ind_to_obj[i]
                else:
                    # those that are new are assigned.
                    self.obj_to_ind[obj] = ind
                    self.ind_to_obj[ind].append(obj)

    def is_equiv(self, *objs):
        """Try to derive if given objects are equivalent, return true
        if so, or false otherwise.
        """
        inds = [self._get_ind(x) for x in objs]
        ind = max(inds)
        if ind != -1:
            return all(i == ind for i in inds)
        else:
            return all([x == objs[0] for x in objs])

    def get_equiv_const(self, obj):
        """Check if obj is equivalent to some int constant, and return
        the constant if found, or None otherwise.
        """
        ind = self._get_ind(obj)
        if ind >= 0:
            objs = self.ind_to_obj[ind]
            for x in objs:
                if isinstance(x, int):
                    return x
        return None

    def get_equiv_set(self, obj):
        """Return the set of equivalent objects.
        """
        ind = self._get_ind(obj)
        if ind >= 0:
            return set(self.ind_to_obj[ind])
        return set()

    def insert_equiv(self, *objs):
        """Insert a set of equivalent objects by modifying self. This
        method can be overloaded to transform object type before insertion.
        """
        self._insert(objs)

    def intersect(self, equiv_set):
        """ Return the intersection of self and the given equiv_set,
        without modifying either of them. The result will also keep
        old equivalence indices unchanged.
        """
        new_set = self.empty()
        new_set.next_ind = self.next_ind

        for objs in equiv_set.ind_to_obj.values():
            inds = tuple(self._get_ind(x) for x in objs)
            ind_to_obj = {}

            for i, x in zip(inds, objs):
                if i in ind_to_obj:
                    ind_to_obj[i].append(x)
                elif i >= 0:
                    ind_to_obj[i] = [x]

            for v in ind_to_obj.values():
                if len(v) > 1:
                    new_set._insert(v)

        return new_set


class ShapeEquivSet(EquivSet):

    """Just like EquivSet, except that it accepts only numba IR variables
    and constants as objects, guided by their types. Arrays are considered
    equivalent as long as their shapes are equivalent. Scalars are
    equivalent only when they are equal in value. Tuples are equivalent
    when they are of the same size, and their elements are equivalent.
    """

    def __init__(self, typemap, defs=None, ind_to_var=None,
                 obj_to_ind=None, ind_to_obj=None, next_id=0):
        """Create a new ShapeEquivSet object, where typemap is a dictionary
        that maps variable names to their types, and it will not be modified.
        Optional keyword arguments are for internal use only.
        """
        self.typemap = typemap
        # defs maps variable name to an int, where
        # 1 means the variable is defined only once, and numbers greater
        # than 1 means defined more than onces.
        self.defs = defs if defs else {}
        # ind_to_var maps index number to a list of variables (of ir.Var type).
        # It is used to retrieve defined shape variables given an equivalence
        # index.
        self.ind_to_var = ind_to_var if ind_to_var else {}

        super(ShapeEquivSet, self).__init__(obj_to_ind, ind_to_obj, next_id)

    def empty(self):
        """Return an empty ShapeEquivSet.
        """
        return ShapeEquivSet(self.typemap, {})

    def clone(self):
        """Return a new copy.
        """
        return ShapeEquivSet(
            self.typemap,
            defs=copy.copy(self.defs),
            ind_to_var=copy.copy(self.ind_to_var),
            obj_to_ind=copy.deepcopy(self.obj_to_ind),
            ind_to_obj=copy.deepcopy(self.ind_to_obj),
            next_id=self.next_ind)

    def __repr__(self):
        return "ShapeEquivSet({}, ind_to_var={})".format(
            self.ind_to_obj, self.ind_to_var)

    def _get_names(self, obj):
        """Return a set of names for the given obj, where array and tuples
        are broken down to their individual shapes or elements. This is
        safe because both Numba array shapes and Python tuples are immutable.
        """
        if isinstance(obj, ir.Var) or isinstance(obj, str):
            name = obj if isinstance(obj, str) else obj.name
            typ = self.typemap[name]
            if (isinstance(typ, types.BaseTuple) or
                    isinstance(typ, types.ArrayCompatible)):
                ndim = (typ.ndim if isinstance(typ, types.ArrayCompatible)
                        else len(typ))
                if ndim == 0:
                    return ()
                else:
                    return tuple("{}#{}".format(name, i) for i in range(ndim))
            else:
                return (name,)
        elif isinstance(obj, ir.Const):
            if isinstance(obj.value, tuple):
                return obj.value
            else:
                return (obj.value,)
        elif isinstance(obj, tuple):
            return tuple(self._get_names(x)[0] for x in obj)
        elif isinstance(obj, int):
            return (obj,)
        else:
            raise NotImplementedError(
                "ShapeEquivSet does not support {}".format(obj))

    def is_equiv(self, *objs):
        """Overload EquivSet.is_equiv to handle Numba IR variables and
        constants.
        """
        assert(len(objs) > 1)
        obj_names = [self._get_names(x) for x in objs]
        obj_names = [x for x in obj_names if x != ()] # rule out 0d shape
        if len(obj_names) <= 1:
            return False;
        ndims = [len(names) for names in obj_names]
        ndim = ndims[0]
        if not all(ndim == x for x in ndims):
            if config.DEBUG_ARRAY_OPT == 1:
                print("is_equiv: Dimension mismatch for {}".format(objs))
            return False
        for i in range(ndim):
            names = [obj_name[i] for obj_name in obj_names]
            if not super(ShapeEquivSet, self).is_equiv(*names):
                return False
        return True

    def get_equiv_const(self, obj):
        """If the given object is equivalent to a constant scalar,
        return the scalar value, or None otherwise.
        """
        names = self._get_names(obj)
        if len(names) > 1:
            return None
        return super(ShapeEquivSet, self).get_equiv_const(names[0])

    def get_equiv_var(self, obj):
        """If the given object is equivalent to some defined variable,
        return the variable, or None otherwise.
        """
        names = self._get_names(obj)
        if len(names) != 1:
            return None
        ind = self._get_ind(names[0])
        vs = self.ind_to_var.get(ind, [])
        return vs[0] if vs != [] else None

    def get_equiv_set(self, obj):
        """Return the set of equivalent objects.
        """
        names = self._get_names(obj)
        if len(names) > 1:
            return None
        return super(ShapeEquivSet, self).get_equiv_set(names[0])

    def _insert(self, objs):
        """Overload EquivSet._insert to manage ind_to_var dictionary.
        """
        inds = []
        for obj in objs:
            if obj in self.obj_to_ind:
                inds.append(self.obj_to_ind[obj])
        varlist = []
        names = set()
        for i in sorted(inds):
            for x in self.ind_to_var[i]:
                if not (x.name in names):
                    varlist.append(x)
                    names.add(x.name)
        super(ShapeEquivSet, self)._insert(objs)
        new_ind = self.obj_to_ind[objs[0]]
        for i in set(inds):
            del self.ind_to_var[i]
        self.ind_to_var[new_ind] = varlist

    def insert_equiv(self, *objs):
        """Overload EquivSet.insert_equiv to handle Numba IR variables and
        constants. Input objs are either variable or constant, and at least
        one of them must be variable.
        """
        assert(len(objs) > 1)
        obj_names = [self._get_names(x) for x in objs]
        obj_names = [x for x in obj_names if x != ()] # rule out 0d shape
        if len(obj_names) <= 1:
            return;
        names = sum([list(x) for x in obj_names], [])
        ndims = [len(x) for x in obj_names]
        ndim = ndims[0]
        assert all(ndim == x for x in ndims), (
            "Dimension mismatch for {}".format(objs))
        varlist = []
        for obj in objs:
            if not isinstance(obj, tuple):
                obj = (obj,)
            for var in obj:
                if isinstance(var, ir.Var) and not (var.name in varlist):
                    # favor those already defined, move to front of varlist
                    if var.name in self.defs:
                        varlist.insert(0, var)
                    else:
                        varlist.append(var)
        # try to populate ind_to_var if variables are present
        for obj in varlist:
            name = obj.name
            if name in names and not (name in self.obj_to_ind):
                self.ind_to_obj[self.next_ind] = [name]
                self.obj_to_ind[name] = self.next_ind
                self.ind_to_var[self.next_ind] = [obj]
                self.next_ind += 1
        for i in range(ndim):
            names = [obj_name[i] for obj_name in obj_names]
            super(ShapeEquivSet, self).insert_equiv(*names)

    def has_shape(self, name):
        """Return true if the shape of the given variable is available.
        """
        return self.get_shape(name) != None

    def get_shape(self, name):
        """Return a tuple of variables that corresponds to the shape
        of the given array, or None if not found.
        """
        return guard(self._get_shape, name)

    def _get_shape(self, name):
        """Return a tuple of variables that corresponds to the shape
        of the given array, or raise GuardException if not found.
        """
        inds = self.get_shape_classes(name)
        require (inds != ())
        shape = []
        for i in inds:
            require(i in self.ind_to_var)
            vs = self.ind_to_var[i]
            require(vs != [])
            shape.append(vs[0])
        return tuple(shape)

    def get_shape_classes(self, name):
        """Instead of the shape tuple, return tuple of int, where
        each int is the corresponding class index of the size object.
        Unknown shapes are given class index -1. Return empty tuple
        if the input name is a scalar variable.
        """
        if isinstance(name, ir.Var):
            name = name.name
        typ = self.typemap[name] if name in self.typemap else None
        if not (isinstance(typ, types.BaseTuple) or
                isinstance(typ, types.SliceType) or
                isinstance(typ, types.ArrayCompatible)):
            return []
        names = self._get_names(name)
        inds = tuple(self._get_ind(name) for name in names)
        return inds

    def intersect(self, equiv_set):
        """Overload the intersect method to handle ind_to_var.
        """
        newset = super(ShapeEquivSet, self).intersect(equiv_set)
        ind_to_var = {}
        for i, objs in newset.ind_to_obj.items():
            assert(len(objs) > 0)
            obj = objs[0]
            assert(obj in self.obj_to_ind)
            assert(obj in equiv_set.obj_to_ind)
            j = self.obj_to_ind[obj]
            k = equiv_set.obj_to_ind[obj]
            assert(j in self.ind_to_var)
            assert(k in equiv_set.ind_to_var)
            varlist = []
            names = [x.name for x in equiv_set.ind_to_var[k]]
            for x in self.ind_to_var[j]:
                if x.name in names:
                    varlist.append(x)
            ind_to_var[i] = varlist
        newset.ind_to_var = ind_to_var
        return newset

    def define(self, name):
        """Increment the internal count of how many times a variable is being
        defined. Most variables in Numba IR are SSA, i.e., defined only once,
        but not all of them. When a variable is being re-defined, it must
        be removed from the equivalence relation.
        """
        if isinstance(name, ir.Var):
            name = name.name
        if name in self.defs:
            self.defs[name] += 1
            # NOTE: variable being redefined, must invalidate previous
            # equivalences. Believe it is a rare case, and only happens to
            # scalar accumuators.
            if name in self.obj_to_ind:
                i = self.obj_to_ind[name]
                del self.obj_to_ind[name]
                self.ind_to_obj[i].remove(name)
                if self.ind_to_obj[i] == []:
                    del self.ind_to_obj[i]
                assert(i in self.ind_to_var)
                names = [x.name for x in self.ind_to_var[i]]
                if name in names:
                    j = names.index(name)
                    del self.ind_to_var[i][j]
                    if self.ind_to_var[i] == []:
                        del self.ind_to_var[i]
                        # no more size variables, remove equivalence too
                        if i in self.ind_to_obj:
                            for obj in self.ind_to_obj[i]:
                                del self.obj_to_ind[obj]
                            del self.ind_to_obj[i]
        else:
            self.defs[name] = 1

    def union_defs(self, defs):
        """Union with the given defs dictionary. This is meant to handle
        branch join-point, where a variable may have been defined in more
        than one branches.
        """
        for k, v in defs.items():
            if v > 0:
                self.define(k)

class SymbolicEquivSet(ShapeEquivSet):

    """Just like ShapeEquivSet, except that it also reasons about variable
    equivalence symbolically by using their arithmetic definitions.
    The goal is to automatically derive the equivalence of array ranges
    (slicing). For instance, a[1:m] and a[0:m-1] shall be considered
    size-equivalence.
    """

    def __init__(self, typemap, def_by=None, ref_by=None, ext_shapes=None,
                 defs=None, ind_to_var=None, obj_to_ind=None,
                 ind_to_obj=None, next_id=0):
        """Create a new SymbolicEquivSet object, where typemap is a dictionary
        that maps variable names to their types, and it will not be modified.
        Optional keyword arguments are for internal use only.
        """
        # A "defined-by" table that maps A to a tuple of (B, i), which
        # means A is defined as: A = B + i, where A,B are variable names,
        # and i is an integer constants.
        self.def_by = def_by if def_by else {}
        # A "refered-by" table that maps A to a list of [(B, i), (C, j) ...],
        # which implies a sequence of definitions: B = A - i, C = A - j, and
        # so on, where A,B,C,... are variable names, and i,j,... are
        # integer constants.
        self.ref_by = ref_by if ref_by else {}
        # A extended shape table that can map an arbitrary object to a shape,
        # currently used to remember shapes for SetItem IR node, and wrapped
        # indices for Slice objects.
        self.ext_shapes = ext_shapes if ext_shapes else {}
        super(SymbolicEquivSet, self).__init__(
            typemap, defs, ind_to_var, obj_to_ind, ind_to_obj, next_id)

    def empty(self):
        """Return an empty SymbolicEquivSet.
        """
        return SymbolicEquivSet(self.typemap)

    def __repr__(self):
        return ("SymbolicEquivSet({}, ind_to_var={}, def_by={}, "
                "ref_by={}, ext_shapes={})".format(self.ind_to_obj,
                self.ind_to_var, self.def_by, self.ref_by, self.ext_shapes))

    def clone(self):
        """Return a new copy.
        """
        return SymbolicEquivSet(
            self.typemap,
            def_by=copy.copy(self.def_by),
            ref_by=copy.copy(self.ref_by),
            ext_shapes=copy.copy(self.ext_shapes),
            defs=copy.copy(self.defs),
            ind_to_var=copy.copy(self.ind_to_var),
            obj_to_ind=copy.deepcopy(self.obj_to_ind),
            ind_to_obj=copy.deepcopy(self.ind_to_obj),
            next_id=self.next_ind)

    def get_rel(self, name):
        """Retrieve a definition pair for the given variable,
        or return None if it is not available.
        """
        return guard(self._get_or_set_rel, name)

    def _get_or_set_rel(self, name, func_ir=None):
        """Retrieve a definition pair for the given variable,
        and if it is not already available, try to look it up
        in the given func_ir, and remember it for future use.
        """
        if isinstance(name, ir.Var):
            name = name.name
        require(self.defs.get(name, 0) == 1)
        if name in self.def_by:
            return self.def_by[name]
        else:
            require(func_ir != None)
            def plus(x, y):
                x_is_const = isinstance(x, int)
                y_is_const = isinstance(y, int)
                if x_is_const:
                    if y_is_const:
                        return x + y
                    else:
                        (var, offset) = y
                        return (var, x + offset)
                else:
                    (var, offset) = x
                    if y_is_const:
                        return (var, y + offset)
                    else:
                        return None
            def minus(x, y):
                if isinstance(y, int):
                    return plus(x, -y)
                elif (isinstance(x, tuple) and isinstance(y, tuple) and
                      x[0] == y[0]):
                    return minus(x[1], y[1])
                else:
                    return None
            expr = get_definition(func_ir, name)
            value = (name, 0) # default to its own name
            if isinstance(expr, ir.Expr):
                if expr.op == 'call':
                    fname, mod_name = find_callname(
                            func_ir, expr, typemap=self.typemap)
                    if fname == 'wrap_index' and mod_name == 'numba.array_analysis':
                        index = tuple(self.obj_to_ind.get(x.name, -1)
                                      for x in expr.args)
                        if -1 in index:
                            return None
                        names = self.ext_shapes.get(index, [])
                        names.append(name)
                        if len(names) > 0:
                            self._insert(names)
                        self.ext_shapes[index] = names
                elif expr.op == 'binop':
                    lhs = self._get_or_set_rel(expr.lhs, func_ir)
                    rhs = self._get_or_set_rel(expr.rhs, func_ir)
                    if expr.fn == operator.add:
                        value = plus(lhs, rhs)
                    elif expr.fn == operator.sub:
                        value = minus(lhs, rhs)
            elif isinstance(expr, ir.Const) and isinstance(expr.value, int):
                value = expr.value
            require(value != None)
            # update def_by table
            self.def_by[name] = value
            if isinstance(value, int) or (isinstance(value, tuple) and
                (value[0] != name or value[1] != 0)):
                # update ref_by table too
                if isinstance(value, tuple):
                    (var, offset) = value
                    if not (var in self.ref_by):
                        self.ref_by[var] = []
                    self.ref_by[var].append((name, -offset))
                    # insert new equivalence if found
                    ind = self._get_ind(var)
                    if ind >= 0:
                        objs = self.ind_to_obj[ind]
                        names = []
                        for obj in objs:
                            if obj in self.ref_by:
                                names += [ x for (x, i) in self.ref_by[obj]
                                           if i == -offset ]
                        if len(names) > 1:
                            super(SymbolicEquivSet, self)._insert(names)
            return value

    def define(self, var, func_ir=None, typ=None):
        """Besides incrementing the definition count of the given variable
        name, it will also retrieve and simplify its definition from func_ir,
        and remember the result for later equivalence comparison. Supported
        operations are:
          1. arithmetic plus and minus with constants
          2. wrap_index (relative to some given size)
        """
        if isinstance(var, ir.Var):
            name = var.name
        else:
            name = var
        super(SymbolicEquivSet, self).define(name)
        if (func_ir and self.defs.get(name, 0) == 1 and
                isinstance(typ, types.Number)):
            value = guard(self._get_or_set_rel, name, func_ir)
            # turn constant definition into equivalence
            if isinstance(value, int):
                self._insert([name, value])
            if isinstance(var, ir.Var):
                ind = self._get_or_add_ind(name)
                if not (ind in self.ind_to_obj):
                    self.ind_to_obj[ind] = [name]
                    self.obj_to_ind[name] = ind
                if ind in self.ind_to_var:
                    self.ind_to_var[ind].append(var)
                else:
                    self.ind_to_var[ind] = [var]

    def _insert(self, objs):
        """Overload _insert method to handle ind changes between relative
        objects.
        """
        indset = set()
        uniqs = set()
        for obj in objs:
            ind = self._get_ind(obj)
            if ind == -1:
                uniqs.add(obj)
            elif not (ind in indset):
                uniqs.add(obj)
                indset.add(ind)
        if len(uniqs) <= 1:
            return
        uniqs = list(uniqs)
        super(SymbolicEquivSet, self)._insert(uniqs)
        objs = self.ind_to_obj[self._get_ind(uniqs[0])]

        # New equivalence guided by def_by and ref_by
        offset_dict = {}
        def get_or_set(d, k):
            if k in d:
                v = d[k]
            else:
                v = []
                d[k] = v
            return v
        for obj in objs:
            if obj in self.def_by:
                value = self.def_by[obj]
                if isinstance(value, tuple):
                    (name, offset) = value
                    get_or_set(offset_dict, -offset).append(name)
                    if name in self.ref_by: # relative to name
                        for (v, i) in self.ref_by[name]:
                            get_or_set(offset_dict, -(offset+i)).append(v)
            if obj in self.ref_by:
                for (name, offset) in self.ref_by[obj]:
                    get_or_set(offset_dict, offset).append(name)
        for names in offset_dict.values():
            self._insert(names)

    def set_shape(self, obj, shape):
        """Overload set_shape to remember shapes of SetItem IR nodes.
        """
        if isinstance(obj, ir.StaticSetItem) or isinstance(obj, ir.SetItem):
            self.ext_shapes[obj] = shape
        else:
            assert(isinstance(obj, ir.Var))
            typ = self.typemap[obj.name]
            super(SymbolicEquivSet, self).set_shape(obj, shape)

    def _get_shape(self, obj):
        """Overload _get_shape to retrieve the shape of SetItem IR nodes.
        """
        if isinstance(obj, ir.StaticSetItem) or isinstance(obj, ir.SetItem):
            require(obj in self.ext_shapes)
            return self.ext_shapes[obj]
        else:
            assert(isinstance(obj, ir.Var))
            typ = self.typemap[obj.name]
            # for slice type, return the shape variable itself
            if isinstance(typ, types.SliceType):
                return (obj,)
            else:
                return super(SymbolicEquivSet, self)._get_shape(obj)

class ArrayAnalysis(object):

    """Analyzes Numpy array computations for properties such as
    shape/size equivalence, and keeps track of them on a per-block
    basis. The analysis should only be run once because it modifies
    the incoming IR by inserting assertion statements that safeguard
    parfor optimizations.
    """

    def __init__(self, context, func_ir, typemap, calltypes):
        self.context = context
        self.func_ir = func_ir
        self.typemap = typemap
        self.calltypes = calltypes

        # EquivSet of variables, indexed by block number
        self.equiv_sets = {}
        # keep attr calls to arrays like t=A.sum() as {t:('sum',A)}
        self.array_attr_calls = {}
        # keep prepended instructions from conditional branch
        self.prepends = {}
        # keep track of pruned precessors when branch degenerates to jump
        self.pruned_predecessors = {}

    def get_equiv_set(self, block_label):
        """Return the equiv_set object of an block given its label.
        """
        return self.equiv_sets[block_label]

    def run(self, blocks=None, equiv_set=None):
        """run array shape analysis on the given IR blocks, resulting in
        modified IR and finalized EquivSet for each block.
        """
        if blocks == None:
            blocks = self.func_ir.blocks

        if equiv_set == None:
            init_equiv_set = SymbolicEquivSet(self.typemap)
        else:
            init_equiv_set = equiv_set

        dprint_func_ir(self.func_ir, "before array analysis", blocks)

        if config.DEBUG_ARRAY_OPT == 1:
            print("variable types: ", sorted(self.typemap.items()))
            print("call types: ", self.calltypes)

        cfg = compute_cfg_from_blocks(blocks)
        topo_order = find_topo_order(blocks, cfg=cfg)
        # Traverse blocks in topological order
        for label in topo_order:
            block = blocks[label]
            scope = block.scope
            new_body = []
            equiv_set = None

            # equiv_set is the intersection of predecessors
            preds = cfg.predecessors(label)
            # some incoming edge may be pruned due to prior analysis
            if label in self.pruned_predecessors:
                pruned = self.pruned_predecessors[label]
            else:
                pruned = []
            # Go through each incoming edge, process prepended instructions and
            # calculate beginning equiv_set of current block as an intersection
            # of incoming ones.
            for (p, q) in preds:
                if p in pruned:
                    continue
                if p in self.equiv_sets:
                    from_set = self.equiv_sets[p].clone()
                    if (p, label) in self.prepends:
                        instrs = self.prepends[(p, label)]
                        for inst in instrs:
                            self._analyze_inst(label, scope, from_set, inst)
                    if equiv_set == None:
                        equiv_set = from_set
                    else:
                        equiv_set = equiv_set.intersect(from_set)
                        equiv_set.union_defs(from_set.defs)

            # Start with a new equiv_set if none is computed
            if equiv_set == None:
                equiv_set = init_equiv_set
            self.equiv_sets[label] = equiv_set
            # Go through instructions in a block, and insert pre/post
            # instructions as we analyze them.
            for inst in block.body:
                pre, post = self._analyze_inst(label, scope, equiv_set, inst)
                for instr in pre:
                    new_body.append(instr)
                new_body.append(inst)
                for instr in post:
                    new_body.append(instr)
            block.body = new_body

        if config.DEBUG_ARRAY_OPT == 1:
            self.dump()

        dprint_func_ir(self.func_ir, "after array analysis", blocks)

    def dump(self):
        """dump per-block equivalence sets for debugging purposes.
        """
        print("Array Analysis: ", self.equiv_sets)

    def _define(self, equiv_set, var, typ, value):
        self.typemap[var.name] = typ
        self.func_ir._definitions[var.name] = [value]
        equiv_set.define(var, self.func_ir, typ)

    def _analyze_inst(self, label, scope, equiv_set, inst):
        pre = []
        post = []
        if isinstance(inst, ir.Assign):
            lhs = inst.target
            typ = self.typemap[lhs.name]
            shape = None
            if isinstance(typ, types.ArrayCompatible) and typ.ndim == 0:
                shape = ()
            elif isinstance(inst.value, ir.Expr):
                result = self._analyze_expr(scope, equiv_set, inst.value)
                if result:
                    shape = result[0]
                    pre = result[1]
                    if len(result) > 2:
                        rhs = result[2]
                        inst.value = rhs
            elif (isinstance(inst.value, ir.Var) or
                  isinstance(inst.value, ir.Const)):
                shape = inst.value

            if isinstance(shape, ir.Const):
                if isinstance(shape.value, tuple):
                    loc = shape.loc
                    shape = tuple(ir.Const(x, loc) for x in shape.value)
                elif isinstance(shape.value, int):
                    shape = (shape,)
                else:
                    shape = None
            elif (isinstance(shape, ir.Var) and
                  isinstance(self.typemap[shape.name], types.Integer)):
                shape = (shape,)

            if isinstance(typ, types.ArrayCompatible):
                if (shape == None or isinstance(shape, tuple) or
                    (isinstance(shape, ir.Var) and
                     not equiv_set.has_shape(shape))):
                    (shape, post) = self._gen_shape_call(equiv_set, lhs,
                                                         typ.ndim, shape)
            elif isinstance(typ, types.UniTuple):
                if shape and isinstance(typ.dtype, types.Integer):
                    (shape, post) = self._gen_shape_call(equiv_set, lhs,
                                                         len(typ), shape)

            if shape != None:
                if isinstance(typ, types.SliceType):
                    equiv_set.set_shape(lhs, shape)
                else:
                    equiv_set.insert_equiv(lhs, shape)
            equiv_set.define(lhs, self.func_ir, typ)
        elif isinstance(inst, ir.StaticSetItem) or isinstance(inst, ir.SetItem):
            index = inst.index if isinstance(inst, ir.SetItem) else inst.index_var
            result = guard(self._index_to_shape,
                scope, equiv_set, inst.target, index)
            if not result:
                return [], []
            (target_shape, pre) = result
            value_shape = equiv_set.get_shape(inst.value)
            if value_shape is (): # constant
                equiv_set.set_shape(inst, target_shape)
                return pre, []
            elif value_shape != None:
                target_typ = self.typemap[inst.target.name]
                require(isinstance(target_typ, types.ArrayCompatible))
                target_ndim = target_typ.ndim
                shapes = [target_shape, value_shape]
                names = [inst.target.name, inst.value.name]
                shape, asserts = self._broadcast_assert_shapes(
                                scope, equiv_set, inst.loc, shapes, names)
                n = len(shape)
                # shape dimension must be within target dimension
                assert(target_ndim >= n)
                equiv_set.set_shape(inst, shape)
                return pre + asserts, []
            else:
                return pre, []
        elif isinstance(inst, ir.Branch):
            cond_var = inst.cond
            cond_def = guard(get_definition, self.func_ir, cond_var)
            if not cond_def:  # phi variable has no single definition
                # We'll use equiv_set to try to find a cond_def instead
                equivs = equiv_set.get_equiv_set(cond_var)
                defs = []
                for name in equivs:
                    if isinstance(name, str) and name in self.typemap:
                        var_def = guard(get_definition, self.func_ir, name,
                                        lhs_only=True)
                        if isinstance(var_def, ir.Var):
                            var_def = var_def.name
                        if var_def:
                            defs.append(var_def)
                    else:
                        defs.append(name)
                defvars = set(filter(lambda x: isinstance(x, str), defs))
                defconsts = set(defs).difference(defvars)
                if len(defconsts) == 1:
                    cond_def = list(defconsts)[0]
                elif len(defvars) == 1:
                    cond_def = guard(get_definition, self.func_ir,
                                     list(defvars)[0])
            if isinstance(cond_def, ir.Expr) and cond_def.op == 'binop':
                br = None
                if cond_def.fn == operator.eq:
                    br = inst.truebr
                    otherbr = inst.falsebr
                    cond_val = 1
                elif cond_def.fn == operator.ne:
                    br = inst.falsebr
                    otherbr = inst.truebr
                    cond_val = 0
                lhs_typ = self.typemap[cond_def.lhs.name]
                rhs_typ = self.typemap[cond_def.rhs.name]
                if (br != None and
                    ((isinstance(lhs_typ, types.Integer) and
                      isinstance(rhs_typ, types.Integer)) or
                     (isinstance(lhs_typ, types.BaseTuple) and
                      isinstance(rhs_typ, types.BaseTuple)))):
                    loc = inst.loc
                    args = (cond_def.lhs, cond_def.rhs)
                    asserts = self._make_assert_equiv(
                        scope, loc, equiv_set, args)
                    asserts.append(
                        ir.Assign(ir.Const(cond_val, loc), cond_var, loc))
                    self.prepends[(label, br)] = asserts
                    self.prepends[(label, otherbr)] = [
                        ir.Assign(ir.Const(1 - cond_val, loc), cond_var, loc)]
            else:
                if isinstance(cond_def, ir.Const):
                    cond_def = cond_def.value
                if isinstance(cond_def, int) or isinstance(cond_def, bool):
                    # condition is always true/false, prune the outgoing edge
                    pruned_br = inst.falsebr if cond_def else inst.truebr
                    if pruned_br in self.pruned_predecessors:
                        self.pruned_predecessors[pruned_br].append(label)
                    else:
                        self.pruned_predecessors[pruned_br] = [label]

        elif type(inst) in array_analysis_extensions:
            # let external calls handle stmt if type matches
            f = array_analysis_extensions[type(inst)]
            pre, post = f(inst, equiv_set, self.typemap, self)

        return pre, post

    def _analyze_expr(self, scope, equiv_set, expr):
        fname = "_analyze_op_{}".format(expr.op)
        try:
            fn = getattr(self, fname)
        except AttributeError:
            return None
        return guard(fn, scope, equiv_set, expr)

    def _analyze_op_getattr(self, scope, equiv_set, expr):
        # TODO: getattr of npytypes.Record
        if expr.attr == 'T' and self._isarray(expr.value.name):
            return self._analyze_op_call_numpy_transpose(scope, equiv_set, [expr.value], {})
        elif expr.attr == 'shape':
            shape = equiv_set.get_shape(expr.value)
            return shape, []
        return None

    def _analyze_op_cast(self, scope, equiv_set, expr):
        return expr.value, []

    def _analyze_op_exhaust_iter(self, scope, equiv_set, expr):
        var = expr.value
        typ = self.typemap[var.name]
        if isinstance(typ, types.BaseTuple):
            require(len(typ) == expr.count)
            require(equiv_set.has_shape(var))
            return var, []
        return None

    def _index_to_shape(self, scope, equiv_set, var, ind_var):
        """For indexing like var[index] (either write or read), see if
        the index corresponds to a range/slice shape. Return the shape
        (and prepending instructions) if so, or raise GuardException
        otherwise.
        """
        typ = self.typemap[var.name]
        require(isinstance(typ, types.ArrayCompatible))
        ind_typ = self.typemap[ind_var.name]
        ind_shape = equiv_set._get_shape(ind_var)
        var_shape = equiv_set._get_shape(var)
        if isinstance(ind_typ, types.SliceType):
            seq_typs = (ind_typ,)
        else:
            require(isinstance(ind_typ, types.BaseTuple))
            seq, op = find_build_sequence(self.func_ir, ind_var)
            require(op == 'build_tuple')
            seq_typs = tuple(self.typemap[x.name] for x in seq)
        require(len(ind_shape)==len(seq_typs)==len(var_shape))
        stmts = []

        def slice_size(index, dsize):
            """Reason about the size of a slice represented by the "index"
            variable, and return a variable that has this size data, or
            raise GuardException if it cannot reason about it.

            The computation takes care of negative values used in the slice
            with respect to the given dimensional size ("dsize").

            Extra statments required to produce the result are appended
            to parent function's stmts list.
            """
            loc = index.loc
            index_def = get_definition(self.func_ir, index)
            fname, mod_name = find_callname(
                self.func_ir, index_def, typemap=self.typemap)
            require(fname == 'slice' and mod_name in ('__builtin__', 'builtins'))
            require(len(index_def.args) == 2)
            lhs = index_def.args[0]
            rhs = index_def.args[1]
            size_typ = self.typemap[dsize.name]
            lhs_typ = self.typemap[lhs.name]
            rhs_typ = self.typemap[rhs.name]
            zero_var = ir.Var(scope, mk_unique_var("zero"), loc)

            if isinstance(lhs_typ, types.NoneType):
                zero = ir.Const(0, loc)
                stmts.append(ir.Assign(value=zero, target=zero_var, loc=loc))
                self._define(equiv_set, zero_var, size_typ, zero)
                lhs = zero_var
                lhs_typ = size_typ

            if isinstance(rhs_typ, types.NoneType):
                rhs = dsize
                rhs_typ = size_typ

            lhs_rel = equiv_set.get_rel(lhs)
            rhs_rel = equiv_set.get_rel(rhs)
            if (lhs_rel == 0 and isinstance(rhs_rel, tuple) and
                equiv_set.is_equiv(dsize, rhs_rel[0]) and
                rhs_rel[1] == 0):
                return dsize

            size_var = ir.Var(scope, mk_unique_var("slice_size"), loc)
            size_val = ir.Expr.binop(operator.sub, rhs, lhs, loc=loc)
            self.calltypes[size_val] = signature(size_typ, lhs_typ, rhs_typ)
            self._define(equiv_set, size_var, size_typ, size_val)

            # short cut size_val to a constant if its relation is known to be
            # a constant or its basis matches dsize
            size_rel = equiv_set.get_rel(size_var)
            if (isinstance(size_rel, int) or (isinstance(size_rel, tuple) and
                equiv_set.is_equiv(size_rel[0], dsize.name))):
                rel = size_rel if isinstance(size_rel, int) else size_rel[1]
                size_val = ir.Const(rel, size_typ)
                size_var = ir.Var(scope, mk_unique_var("slice_size"), loc)
                self._define(equiv_set, size_var, size_typ, size_val)

            wrap_var = ir.Var(scope, mk_unique_var("wrap"), loc)
            wrap_def = ir.Global('wrap_index', wrap_index, loc=loc)
            fnty = get_global_func_typ(wrap_index)
            sig = self.context.resolve_function_type(fnty, (size_typ, size_typ,), {})
            self._define(equiv_set, wrap_var, fnty, wrap_def)

            var = ir.Var(scope, mk_unique_var("var"), loc)
            value = ir.Expr.call(wrap_var, [size_var, dsize], {}, loc)
            self._define(equiv_set, var, size_typ, value)
            self.calltypes[value] = sig

            stmts.append(ir.Assign(value=size_val, target=size_var, loc=loc))
            stmts.append(ir.Assign(value=wrap_def, target=wrap_var, loc=loc))
            stmts.append(ir.Assign(value=value, target=var, loc=loc))
            return var

        def to_shape(typ, index, dsize):
            if isinstance(typ, types.SliceType):
                return slice_size(index, dsize)
            elif isinstance(typ, types.Number):
                return None
            else:
                # unknown dimension size for this index,
                # so we'll raise GuardException
                require(False)
        shape = tuple(to_shape(typ, size, dsize) for
                      (typ, size, dsize) in zip(seq_typs, ind_shape, var_shape))
        require(not all(x == None for x in shape))
        shape = tuple(x for x in shape if x != None)
        return shape, stmts

    def _analyze_op_getitem(self, scope, equiv_set, expr):
        return self._index_to_shape(scope, equiv_set, expr.value, expr.index)

    def _analyze_op_static_getitem(self, scope, equiv_set, expr):
        var = expr.value
        typ = self.typemap[var.name]
        if not isinstance(typ, types.BaseTuple):
            return self._index_to_shape(scope, equiv_set, expr.value, expr.index_var)
        shape = equiv_set._get_shape(var)
        require(isinstance(expr.index, int) and expr.index < len(shape))
        return shape[expr.index], []

    def _analyze_op_unary(self, scope, equiv_set, expr):
        require(expr.fn in UNARY_MAP_OP)
        # for scalars, only + operator results in equivalence
        # for example, if "m = -n", m and n are not equivalent
        if self._isarray(expr.value.name) or expr.fn == operator.add:
            return expr.value, []
        return None

    def _analyze_op_binop(self, scope, equiv_set, expr):
        require(expr.fn in BINARY_MAP_OP)
        return self._analyze_broadcast(scope, equiv_set, expr.loc, [expr.lhs, expr.rhs])

    def _analyze_op_inplace_binop(self, scope, equiv_set, expr):
        require(expr.fn in INPLACE_BINARY_MAP_OP)
        return self._analyze_broadcast(scope, equiv_set, expr.loc, [expr.lhs, expr.rhs])

    def _analyze_op_arrayexpr(self, scope, equiv_set, expr):
        return self._analyze_broadcast(scope, equiv_set, expr.loc, expr.list_vars())

    def _analyze_op_build_tuple(self, scope, equiv_set, expr):
        return tuple(expr.items), []

    def _analyze_op_call(self, scope, equiv_set, expr):
        from numba.stencil import StencilFunc

        callee = expr.func
        callee_def = get_definition(self.func_ir, callee)
        if (isinstance(callee_def, (ir.Global, ir.FreeVar))
                and is_namedtuple_class(callee_def.value)):
            return tuple(expr.args), []
        if (isinstance(callee_def, (ir.Global, ir.FreeVar))
                and isinstance(callee_def.value, StencilFunc)):
            args = expr.args
            return self._analyze_stencil(scope, equiv_set, callee_def.value,
                                         expr.loc, args, dict(expr.kws))

        fname, mod_name = find_callname(
            self.func_ir, expr, typemap=self.typemap)
        # call via attribute (i.e. array.func)
        if (isinstance(mod_name, ir.Var)
                and isinstance(self.typemap[mod_name.name],
                                types.ArrayCompatible)):
            args = [mod_name] + expr.args
            mod_name = 'numpy'
        else:
            args = expr.args
        fname = "_analyze_op_call_{}_{}".format(
            mod_name, fname).replace('.', '_')
        if fname in UFUNC_MAP_OP:  # known numpy ufuncs
            return self._analyze_broadcast(scope, equiv_set, expr.loc, args)
        else:
            try:
                fn = getattr(self, fname)
            except AttributeError:
                return None
            return guard(fn, scope, equiv_set, args, dict(expr.kws))

    def _analyze_op_call___builtin___len(self, scope, equiv_set, args, kws):
        # python 2 version of len()
        return self._analyze_op_call_builtins_len(scope, equiv_set, args, kws)

    def _analyze_op_call_builtins_len(self, scope, equiv_set, args, kws):
        # python 3 version of len()
        require(len(args) == 1)
        var = args[0]
        typ = self.typemap[var.name]
        require(isinstance(typ, types.ArrayCompatible))
        if typ.ndim == 1:
            shape = equiv_set._get_shape(var)
            return shape[0], [], shape[0]
        return None

    def _analyze_op_call_numba_array_analysis_assert_equiv(self, scope,
                                                        equiv_set, args, kws):
        equiv_set.insert_equiv(*args[1:])
        return None

    def _analyze_numpy_create_array(self, scope, equiv_set, args, kws):
        shape_var = None
        if len(args) > 0:
            shape_var = args[0]
        elif 'shape' in kws:
            shape_var = kws['shape']
        if shape_var:
            return shape_var, []
        raise NotImplementedError("Must specify a shape for array creation")

    def _analyze_op_call_numpy_empty(self, scope, equiv_set, args, kws):
        return self._analyze_numpy_create_array(scope, equiv_set, args, kws)

    def _analyze_op_call_numba_unsafe_ndarray_empty_inferred(self, scope,
                                                         equiv_set, args, kws):
        return self._analyze_numpy_create_array(scope, equiv_set, args, kws)

    def _analyze_op_call_numpy_zeros(self, scope, equiv_set, args, kws):
        return self._analyze_numpy_create_array(scope, equiv_set, args, kws)

    def _analyze_op_call_numpy_ones(self, scope, equiv_set, args, kws):
        return self._analyze_numpy_create_array(scope, equiv_set, args, kws)

    def _analyze_op_call_numpy_eye(self, scope, equiv_set, args, kws):
        if len(args) > 0:
            N = args[0]
        elif 'N' in kws:
            N = kws['N']
        else:
            raise NotImplementedError(
                "Expect one argument (or 'N') to eye function")
        if 'M' in kws:
            M = kws['M']
        else:
            M = N
        return (N, M), []

    def _analyze_op_call_numpy_identity(self, scope, equiv_set, args, kws):
        assert len(args) > 0
        N = args[0]
        return (N, N), []

    def _analyze_op_call_numpy_diag(self, scope, equiv_set, args, kws):
        # We can only reason about the output shape when the input is 1D or
        # square 2D.
        assert len(args) > 0
        a = args[0]
        assert(isinstance(a, ir.Var))
        atyp = self.typemap[a.name]
        if isinstance(atyp, types.ArrayCompatible):
            if atyp.ndim == 2:
                if 'k' in kws:  # will proceed only when k = 0 or absent
                    k = kws['k']
                    if not equiv_set.is_equiv(k, 0):
                        return None
                (m, n) = equiv_set._get_shape(a)
                if equiv_set.is_equiv(m, n):
                    return (m,), []
            elif atyp.ndim == 1:
                (m,) = equiv_set._get_shape(a)
                return (m, m), []
        return None

    def _analyze_numpy_array_like(self, scope, equiv_set, args, kws):
        assert(len(args) > 0)
        var = args[0]
        typ = self.typemap[var.name]
        if isinstance(typ, types.Integer):
            return (1,), []
        elif (isinstance(typ, types.ArrayCompatible) and
              equiv_set.has_shape(var)):
            return var, []
        return None

    def _analyze_op_call_numpy_ravel(self, scope, equiv_set, args, kws):
        assert(len(args) == 1)
        var = args[0]
        typ = self.typemap[var.name]
        assert isinstance(typ, types.ArrayCompatible)
        # output array is same shape as input if input is 1D
        if typ.ndim == 1 and equiv_set.has_shape(var):
            if typ.layout == 'C':
                # output is the same as input (no copy) for 'C' layout
                # optimize out the call
                return var, [], var
            else:
                return var, []
        # TODO: handle multi-D input arrays (calc array size)
        return None

    def _analyze_op_call_numpy_copy(self, *args):
        return self._analyze_numpy_array_like(*args)

    def _analyze_op_call_numpy_empty_like(self, *args):
        return self._analyze_numpy_array_like(*args)

    def _analyze_op_call_numpy_zeros_like(self, *args):
        return self._analyze_numpy_array_like(*args)

    def _analyze_op_call_numpy_ones_like(self, *args):
        return self._analyze_numpy_array_like(*args)

    def _analyze_op_call_numpy_full_like(self, *args):
        return self._analyze_numpy_array_like(*args)

    def _analyze_op_call_numpy_asfortranarray(self, *args):
        return self._analyze_numpy_array_like(*args)

    def _analyze_op_call_numpy_reshape(self, scope, equiv_set, args, kws):
        n = len(args)
        assert(n > 1)
        if n == 2:
            typ = self.typemap[args[1].name]
            if isinstance(typ, types.BaseTuple):
                return args[1], []
        return tuple(args[1:]), []

    def _analyze_op_call_numpy_transpose(self, scope, equiv_set, args, kws):
        in_arr = args[0]
        typ = self.typemap[in_arr.name]
        assert isinstance(typ, types.ArrayCompatible), \
            "Invalid np.transpose argument"
        shape = equiv_set._get_shape(in_arr)
        if len(args) == 1:
            return tuple(reversed(shape)), []
        axes = [guard(find_const, self.func_ir, a) for a in args[1:]]
        if isinstance(axes[0], tuple):
            axes = list(axes[0])
        if None in axes:
            return None
        ret = [shape[i] for i in axes]
        return tuple(ret), []

    def _analyze_op_call_numpy_random_rand(self, scope, equiv_set, args, kws):
        if len(args) > 0:
            return tuple(args), []
        return None

    def _analyze_op_call_numpy_random_randn(self, *args):
        return self._analyze_op_call_numpy_random_rand(*args)

    def _analyze_op_numpy_random_with_size(self, pos, scope, equiv_set, args, kws):
        if 'size' in kws:
            return kws['size'], []
        if len(args) > pos:
            return args[pos], []
        return None

    def _analyze_op_call_numpy_random_ranf(self, *args):
        return self._analyze_op_numpy_random_with_size(0, *args)

    def _analyze_op_call_numpy_random_random_sample(self, *args):
        return self._analyze_op_numpy_random_with_size(0, *args)

    def _analyze_op_call_numpy_random_sample(self, *args):
        return self._analyze_op_numpy_random_with_size(0, *args)

    def _analyze_op_call_numpy_random_random(self, *args):
        return self._analyze_op_numpy_random_with_size(0, *args)

    def _analyze_op_call_numpy_random_standard_normal(self, *args):
        return self._analyze_op_numpy_random_with_size(0, *args)

    def _analyze_op_call_numpy_random_chisquare(self, *args):
        return self._analyze_op_numpy_random_with_size(1, *args)

    def _analyze_op_call_numpy_random_weibull(self, *args):
        return self._analyze_op_numpy_random_with_size(1, *args)

    def _analyze_op_call_numpy_random_power(self, *args):
        return self._analyze_op_numpy_random_with_size(1, *args)

    def _analyze_op_call_numpy_random_geometric(self, *args):
        return self._analyze_op_numpy_random_with_size(1, *args)

    def _analyze_op_call_numpy_random_exponential(self, *args):
        return self._analyze_op_numpy_random_with_size(1, *args)

    def _analyze_op_call_numpy_random_poisson(self, *args):
        return self._analyze_op_numpy_random_with_size(1, *args)

    def _analyze_op_call_numpy_random_rayleigh(self, *args):
        return self._analyze_op_numpy_random_with_size(1, *args)

    def _analyze_op_call_numpy_random_normal(self, *args):
        return self._analyze_op_numpy_random_with_size(2, *args)

    def _analyze_op_call_numpy_random_uniform(self, *args):
        return self._analyze_op_numpy_random_with_size(2, *args)

    def _analyze_op_call_numpy_random_beta(self, *args):
        return self._analyze_op_numpy_random_with_size(2, *args)

    def _analyze_op_call_numpy_random_binomial(self, *args):
        return self._analyze_op_numpy_random_with_size(2, *args)

    def _analyze_op_call_numpy_random_f(self, *args):
        return self._analyze_op_numpy_random_with_size(2, *args)

    def _analyze_op_call_numpy_random_gamma(self, *args):
        return self._analyze_op_numpy_random_with_size(2, *args)

    def _analyze_op_call_numpy_random_lognormal(self, *args):
        return self._analyze_op_numpy_random_with_size(2, *args)

    def _analyze_op_call_numpy_random_laplace(self, *args):
        return self._analyze_op_numpy_random_with_size(2, *args)

    def _analyze_op_call_numpy_random_randint(self, *args):
        return self._analyze_op_numpy_random_with_size(2, *args)

    def _analyze_op_call_numpy_random_triangular(self, *args):
        return self._analyze_op_numpy_random_with_size(3, *args)

    def _analyze_op_call_numpy_concatenate(self, scope, equiv_set, args, kws):
        assert(len(args) > 0)
        loc = args[0].loc
        seq, op = find_build_sequence(self.func_ir, args[0])
        n = len(seq)
        require(n > 0)
        axis = 0
        if 'axis' in kws:
            if isinstance(kws['axis'], int):  # internal use only
                axis = kws['axis']
            else:
                axis = find_const(self.func_ir, kws['axis'])
        elif len(args) > 1:
            axis = find_const(self.func_ir, args[1])
        require(isinstance(axis, int))
        require(op == 'build_tuple')
        shapes = [equiv_set._get_shape(x) for x in seq]
        if axis < 0:
            axis = len(shapes[0]) + axis
        require(0 <= axis < len(shapes[0]))
        asserts = []
        new_shape = []
        if n == 1:  # from one array N-dimension to (N-1)-dimension
            shape = shapes[0]
            # first size is the count, pop it out of shapes
            n = equiv_set.get_equiv_const(shapes[0])
            shape.pop(0)
            for i in range(len(shape)):
                if i == axis:
                    m = equiv_set.get_equiv_const(shape[i])
                    size = m * n if (m and n) else None
                else:
                    size = self._sum_size(equiv_set, shapes[0])
            new_shape.append(size)
        else:  # from n arrays N-dimension to N-dimension
            for i in range(len(shapes[0])):
                if i == axis:
                    size = self._sum_size(
                        equiv_set, [shape[i] for shape in shapes])
                else:
                    sizes = [shape[i] for shape in shapes]
                    asserts.append(
                        self._call_assert_equiv(scope, loc, equiv_set, sizes))
                    size = sizes[0]
                new_shape.append(size)
        return tuple(new_shape), sum(asserts, [])

    def _analyze_op_call_numpy_stack(self, scope, equiv_set, args, kws):
        assert(len(args) > 0)
        loc = args[0].loc
        seq, op = find_build_sequence(self.func_ir, args[0])
        n = len(seq)
        require(n > 0)
        axis = 0
        if 'axis' in kws:
            if isinstance(kws['axis'], int):  # internal use only
                axis = kws['axis']
            else:
                axis = find_const(self.func_ir, kws['axis'])
        elif len(args) > 1:
            axis = find_const(self.func_ir, args[1])
        require(isinstance(axis, int))
        # only build_tuple can give reliable count
        require(op == 'build_tuple')
        shapes = [equiv_set._get_shape(x) for x in seq]
        asserts = self._call_assert_equiv(scope, loc, equiv_set, seq)
        shape = shapes[0]
        if axis < 0:
            axis = len(shape) + axis + 1
        require(0 <= axis <= len(shape))
        new_shape = list(shape[0:axis]) + [n] + list(shape[axis:])
        return tuple(new_shape), asserts

    def _analyze_op_call_numpy_vstack(self, scope, equiv_set, args, kws):
        assert(len(args) == 1)
        seq, op = find_build_sequence(self.func_ir, args[0])
        n = len(seq)
        require(n > 0)
        typ = self.typemap[seq[0].name]
        require(isinstance(typ, types.ArrayCompatible))
        if typ.ndim < 2:
            return self._analyze_op_call_numpy_stack(scope, equiv_set, args, kws)
        else:
            kws['axis'] = 0
            return self._analyze_op_call_numpy_concatenate(scope, equiv_set, args, kws)

    def _analyze_op_call_numpy_hstack(self, scope, equiv_set, args, kws):
        assert(len(args) == 1)
        seq, op = find_build_sequence(self.func_ir, args[0])
        n = len(seq)
        require(n > 0)
        typ = self.typemap[seq[0].name]
        require(isinstance(typ, types.ArrayCompatible))
        if typ.ndim < 2:
            kws['axis'] = 0
        else:
            kws['axis'] = 1
        return self._analyze_op_call_numpy_concatenate(scope, equiv_set, args, kws)

    def _analyze_op_call_numpy_dstack(self, scope, equiv_set, args, kws):
        assert(len(args) == 1)
        seq, op = find_build_sequence(self.func_ir, args[0])
        n = len(seq)
        require(n > 0)
        typ = self.typemap[seq[0].name]
        require(isinstance(typ, types.ArrayCompatible))
        if typ.ndim == 1:
            kws['axis'] = 1
            result = self._analyze_op_call_numpy_stack(
                scope, equiv_set, args, kws)
            require(result)
            (shape, pre) = result
            shape = tuple([1] + list(shape))
            return shape, pre
        elif typ.ndim == 2:
            kws['axis'] = 2
            return self._analyze_op_call_numpy_stack(scope, equiv_set, args, kws)
        else:
            kws['axis'] = 2
            return self._analyze_op_call_numpy_concatenate(scope, equiv_set, args, kws)

    def _analyze_op_call_numpy_cumsum(self, scope, equiv_set, args, kws):
        # TODO
        return None

    def _analyze_op_call_numpy_cumprod(self, scope, equiv_set, args, kws):
        # TODO
        return None

    def _analyze_op_call_numpy_linspace(self, scope, equiv_set, args, kws):
        n = len(args)
        num = 50
        if n > 2:
            num = args[2]
        elif 'num' in kws:
            num = kws['num']
        return (num,), []

    def _analyze_op_call_numpy_dot(self, scope, equiv_set, args, kws):
        n = len(args)
        assert(n >= 2)
        loc = args[0].loc
        require(all([self._isarray(x.name) for x in args]))
        typs = [self.typemap[x.name] for x in args]
        dims = [ty.ndim for ty in typs]
        require(all(x > 0 for x in dims))
        if dims[0] == 1 and dims[1] == 1:
            return None
        shapes = [equiv_set._get_shape(x) for x in args]
        if dims[0] == 1:
            asserts = self._call_assert_equiv(
                scope, loc, equiv_set, [shapes[0][0], shapes[1][-2]])
            return tuple(shapes[1][0:-2] + shapes[1][-1:]), asserts
        if dims[1] == 1:
            asserts = self._call_assert_equiv(
                scope, loc, equiv_set, [shapes[0][-1], shapes[1][0]])
            return tuple(shapes[0][0:-1]), asserts
        if dims[0] == 2 and dims[1] == 2:
            asserts = self._call_assert_equiv(
                scope, loc, equiv_set, [shapes[0][1], shapes[1][0]])
            return (shapes[0][0], shapes[1][1]), asserts
        if dims[0] > 2:  # TODO: handle higher dimension cases
            pass
        return None

    def _analyze_stencil(self, scope, equiv_set, stencil_func, loc, args, kws):
        # stencil requires that all relatively indexed array arguments are
        # of same size
        std_idx_arrs = stencil_func.options.get('standard_indexing', ())
        kernel_arg_names = stencil_func.kernel_ir.arg_names
        if isinstance(std_idx_arrs, str):
            std_idx_arrs = (std_idx_arrs,)
        rel_idx_arrs = []
        assert(len(args) > 0 and len(args) == len(kernel_arg_names))
        for arg, var in zip(kernel_arg_names, args):
            typ = self.typemap[var.name]
            if (isinstance(typ, types.ArrayCompatible) and
                not(arg in std_idx_arrs)):
                rel_idx_arrs.append(var)
        n = len(rel_idx_arrs)
        require(n > 0)
        asserts = self._call_assert_equiv(scope, loc, equiv_set, rel_idx_arrs)
        shape = equiv_set.get_shape(rel_idx_arrs[0])
        return shape, asserts

    def _analyze_op_call_numpy_linalg_inv(self, scope, equiv_set, args, kws):
        require(len(args) >= 1)
        return equiv_set._get_shape(args[0]), []

    def _analyze_broadcast(self, scope, equiv_set, loc, args):
        """Infer shape equivalence of arguments based on Numpy broadcast rules
        and return shape of output
        https://docs.scipy.org/doc/numpy/user/basics.broadcasting.html
        """
        arrs = list(filter(lambda a: self._isarray(a.name), args))
        require(len(arrs) > 0)
        names = [x.name for x in arrs]
        dims = [self.typemap[x.name].ndim for x in arrs]
        max_dim = max(dims)
        require(max_dim > 0)
        try:
            shapes = [equiv_set.get_shape(x) for x in arrs]
        except GuardException:
            return arrs[0], self._call_assert_equiv(scope, loc, equiv_set, arrs)
        return self._broadcast_assert_shapes(scope, equiv_set, loc, shapes, names)

    def _broadcast_assert_shapes(self, scope, equiv_set, loc, shapes, names):
        """Produce assert_equiv for sizes in each dimension, taking into account
        of dimension coercion and constant size of 1.
        """
        asserts = []
        new_shape = []
        max_dim = max([len(shape) for shape in shapes])
        const_size_one = None
        for i in range(max_dim):
            sizes = []
            size_names = []
            for name, shape in zip(names, shapes):
                if i < len(shape):
                    size = shape[len(shape) - 1 - i]
                    const_size = equiv_set.get_equiv_const(size)
                    if const_size == 1:
                        const_size_one = size
                    else:
                        sizes.append(size)  # non-1 size to front
                        size_names.append(name)
            if sizes == []:
                assert(const_size_one != None)
                sizes.append(const_size_one)
                size_names.append("1")
            asserts.append(self._call_assert_equiv(scope, loc, equiv_set,
                                                   sizes, names=size_names))
            new_shape.append(sizes[0])
        return tuple(reversed(new_shape)), sum(asserts, [])

    def _call_assert_equiv(self, scope, loc, equiv_set, args, names=None):
        insts = self._make_assert_equiv(
            scope, loc, equiv_set, args, names=names)
        if len(args) > 1:
            equiv_set.insert_equiv(*args)
        return insts

    def _make_assert_equiv(self, scope, loc, equiv_set, _args, names=None):
        # filter out those that are already equivalent
        if names == None:
            names = [x.name for x in _args]
        args = []
        arg_names = []
        for name, x in zip(names, _args):
            seen = False
            for y in args:
                if equiv_set.is_equiv(x, y):
                    seen = True
                    break
            if not seen:
                args.append(x)
                arg_names.append(name)

        # no assertion necessary if there are less than two
        if len(args) < 2:
            return []

        msg = "Sizes of {} do not match on {}".format(', '.join(arg_names), loc)
        msg_val = ir.Const(msg, loc)
        msg_typ = types.StringLiteral(msg)
        msg_var = ir.Var(scope, mk_unique_var("msg"), loc)
        self.typemap[msg_var.name] = msg_typ
        argtyps = tuple([msg_typ] + [self.typemap[x.name] for x in args])

        # assert_equiv takes vararg, which requires a tuple as argument type
        tup_typ = types.BaseTuple.from_types(argtyps)

        # prepare function variable whose type may vary since it takes vararg
        assert_var = ir.Var(scope, mk_unique_var("assert"), loc)
        assert_def = ir.Global('assert_equiv', assert_equiv, loc=loc)
        fnty = get_global_func_typ(assert_equiv)
        sig = self.context.resolve_function_type(fnty, (tup_typ,), {})
        self._define(equiv_set, assert_var, fnty, assert_def)

        # The return value from assert_equiv is always of none type.
        var = ir.Var(scope, mk_unique_var("ret"), loc)
        value = ir.Expr.call(assert_var, [msg_var] + args, {}, loc=loc)
        self._define(equiv_set, var, types.none, value)
        self.calltypes[value] = sig

        return [ir.Assign(value=msg_val, target=msg_var, loc=loc),
                ir.Assign(value=assert_def, target=assert_var, loc=loc),
                ir.Assign(value=value, target=var, loc=loc),
                ]

    def _gen_shape_call(self, equiv_set, var, ndims, shape):
        out = []
        # attr call: A_sh_attr = getattr(A, shape)
        if isinstance(shape, ir.Var):
            shape = equiv_set.get_shape(shape)
        # already a tuple variable that contains size
        if isinstance(shape, ir.Var):
            attr_var = shape
            shape_attr_call = None
            shape = None
        else:
            shape_attr_call = ir.Expr.getattr(var, "shape", var.loc)
            attr_var = ir.Var(var.scope, mk_unique_var(
                              "{}_shape".format(var.name)), var.loc)
            shape_attr_typ = types.containers.UniTuple(types.intp, ndims)
        size_vars = []
        use_attr_var = False
        # trim shape tuple if it is more than ndim
        if shape:
            nshapes = len(shape)
            if ndims < nshapes:
                shape = shape[(nshapes-ndims):]
        for i in range(ndims):
            skip = False
            if shape and shape[i]:
                if isinstance(shape[i], ir.Var):
                    typ = self.typemap[shape[i].name]
                    if (isinstance(typ, types.Number) or
                        isinstance(typ, types.SliceType)):
                        size_var = shape[i]
                        skip = True
                else:
                    if isinstance(shape[i], int):
                        size_val = ir.Const(shape[i], var.loc)
                    else:
                        size_val = shape[i]
                    assert(isinstance(size_val, ir.Const))
                    size_var = ir.Var(var.scope, mk_unique_var(
                        "{}_size{}".format(var.name, i)), var.loc)
                    out.append(ir.Assign(size_val, size_var, var.loc))
                    self._define(equiv_set, size_var, types.intp, size_val)
                    skip = True
            if not skip:
                # get size: Asize0 = A_sh_attr[0]
                size_var = ir.Var(var.scope, mk_unique_var(
                                  "{}_size{}".format(var.name, i)), var.loc)
                getitem = ir.Expr.static_getitem(attr_var, i, None, var.loc)
                use_attr_var = True
                self.calltypes[getitem] = None
                out.append(ir.Assign(getitem, size_var, var.loc))
                self._define(equiv_set, size_var, types.intp, getitem)
            size_vars.append(size_var)
        if use_attr_var and shape_attr_call:
            # only insert shape call if there is any getitem call
            out.insert(0, ir.Assign(shape_attr_call, attr_var, var.loc))
            self._define(equiv_set, attr_var, shape_attr_typ, shape_attr_call)
        return tuple(size_vars), out

    def _isarray(self, varname):
        # no SmartArrayType support yet (can't generate parfor, allocate, etc)
        typ = self.typemap[varname]
        return (isinstance(typ, types.npytypes.Array) and
                not isinstance(typ, types.npytypes.SmartArrayType) and
                typ.ndim > 0)

    def _sum_size(self, equiv_set, sizes):
        """Return the sum of the given list of sizes if they are all equivalent
        to some constant, or None otherwise.
        """
        s = 0
        for size in sizes:
            n = equiv_set.get_equiv_const(size)
            if n == None:
                return None
            else:
                s += n
        return s

UNARY_MAP_OP = list(
    npydecl.NumpyRulesUnaryArrayOperator._op_map.keys()) + [operator.pos]
BINARY_MAP_OP = npydecl.NumpyRulesArrayOperator._op_map.keys()
INPLACE_BINARY_MAP_OP = npydecl.NumpyRulesInplaceArrayOperator._op_map.keys()
UFUNC_MAP_OP = [f.__name__ for f in npydecl.supported_ufuncs]
