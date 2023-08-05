from __future__ import division

import itertools

import numpy as np

from numba import unittest_support as unittest
from numba import jit, typeof, types
from numba.compiler import compile_isolated
from .support import TestCase, CompilationCache, MemoryLeakMixin, tag


def array_iter(arr):
    total = 0
    for i, v in enumerate(arr):
        total += i * v
    return total

def array_view_iter(arr, idx):
    total = 0
    for i, v in enumerate(arr[idx]):
        total += i * v
    return total

def array_flat(arr, out):
    for i, v in enumerate(arr.flat):
        out[i] = v

def array_flat_getitem(arr, ind):
    return arr.flat[ind]

def array_flat_setitem(arr, ind, val):
    arr.flat[ind] = val

def array_flat_sum(arr):
    s = 0
    for i, v in enumerate(arr.flat):
        s = s + (i + 1) * v
    return s

def array_flat_len(arr):
    return len(arr.flat)

def array_ndenumerate_sum(arr):
    s = 0
    for (i, j), v in np.ndenumerate(arr):
        s = s + (i + 1) * (j + 1) * v
    return s

def np_ndindex_empty():
    s = 0
    for ind in np.ndindex(()):
        s += s + len(ind) + 1
    return s

def np_ndindex(x, y):
    s = 0
    n = 0
    for i, j in np.ndindex(x, y):
        s = s + (i + 1) * (j + 1)
    return s

def np_ndindex_array(arr):
    s = 0
    n = 0
    for indices in np.ndindex(arr.shape):
        for i, j in enumerate(indices):
            s = s + (i + 1) * (j + 1)
    return s

def np_nditer1(a):
    res = []
    for u in np.nditer(a):
        res.append(u.item())
    return res

def np_nditer2(a, b):
    res = []
    for u, v in np.nditer((a, b)):
        res.append((u.item(), v.item()))
    return res

def np_nditer3(a, b, c):
    res = []
    for u, v, w in np.nditer((a, b, c)):
        res.append((u.item(), v.item(), w.item()))
    return res

def iter_next(arr):
    it = iter(arr)
    it2 = iter(arr)
    return next(it), next(it), next(it2)


#
# Test premature free (see issue #2112).
# The following test allocates an array ``x`` inside the body.
# The compiler will put a ``del x`` right after the last use of ``x``,
# which is right after the creation of the array iterator and
# before the loop is entered.  If the iterator does not incref the array,
# the iterator will be reading garbage data of free'ed memory.
#

def array_flat_premature_free(size):
    x = np.arange(size)
    res = np.zeros_like(x, dtype=np.intp)
    for i, v in enumerate(x.flat):
        res[i] = v
    return res

def array_ndenumerate_premature_free(size):
    x = np.arange(size)
    res = np.zeros_like(x, dtype=np.intp)
    for i, v in np.ndenumerate(x):
        res[i] = v
    return res


class TestArrayIterators(MemoryLeakMixin, TestCase):
    """
    Test array.flat, np.ndenumerate(), etc.
    """

    def setUp(self):
        super(TestArrayIterators, self).setUp()
        self.ccache = CompilationCache()

    def check_array_iter(self, arr):
        pyfunc = array_iter
        cres = compile_isolated(pyfunc, [typeof(arr)])
        cfunc = cres.entry_point
        expected = pyfunc(arr)
        self.assertPreciseEqual(cfunc(arr), expected)

    def check_array_view_iter(self, arr, index):
        pyfunc = array_view_iter
        cres = compile_isolated(pyfunc, [typeof(arr), typeof(index)])
        cfunc = cres.entry_point
        expected = pyfunc(arr, index)
        self.assertPreciseEqual(cfunc(arr, index), expected)

    def check_array_flat(self, arr, arrty=None):
        out = np.zeros(arr.size, dtype=arr.dtype)
        nb_out = out.copy()
        if arrty is None:
            arrty = typeof(arr)

        cres = compile_isolated(array_flat, [arrty, typeof(out)])
        cfunc = cres.entry_point

        array_flat(arr, out)
        cfunc(arr, nb_out)

        self.assertPreciseEqual(out, nb_out)

    def check_array_unary(self, arr, arrty, func):
        cres = compile_isolated(func, [arrty])
        cfunc = cres.entry_point
        self.assertPreciseEqual(cfunc(arr), func(arr))

    def check_array_flat_sum(self, arr, arrty):
        self.check_array_unary(arr, arrty, array_flat_sum)

    def check_array_ndenumerate_sum(self, arr, arrty):
        self.check_array_unary(arr, arrty, array_ndenumerate_sum)

    @tag('important')
    def test_array_iter(self):
        # Test iterating over a 1d array
        arr = np.arange(6)
        self.check_array_iter(arr)
        arr = arr[::2]
        self.assertFalse(arr.flags.c_contiguous)
        self.assertFalse(arr.flags.f_contiguous)
        self.check_array_iter(arr)
        arr = np.bool_([1, 0, 0, 1])
        self.check_array_iter(arr)

    def test_array_view_iter(self):
        # Test iterating over a 1d view over a 2d array
        arr = np.arange(12).reshape((3, 4))
        self.check_array_view_iter(arr, 1)
        self.check_array_view_iter(arr.T, 1)
        arr = arr[::2]
        self.check_array_view_iter(arr, 1)
        arr = np.bool_([1, 0, 0, 1]).reshape((2, 2))
        self.check_array_view_iter(arr, 1)

    @tag('important')
    def test_array_flat_3d(self):
        arr = np.arange(24).reshape(4, 2, 3)

        arrty = typeof(arr)
        self.assertEqual(arrty.ndim, 3)
        self.assertEqual(arrty.layout, 'C')
        self.assertTrue(arr.flags.c_contiguous)
        # Test with C-contiguous array
        self.check_array_flat(arr)
        # Test with Fortran-contiguous array
        arr = arr.transpose()
        self.assertFalse(arr.flags.c_contiguous)
        self.assertTrue(arr.flags.f_contiguous)
        self.assertEqual(typeof(arr).layout, 'F')
        self.check_array_flat(arr)
        # Test with non-contiguous array
        arr = arr[::2]
        self.assertFalse(arr.flags.c_contiguous)
        self.assertFalse(arr.flags.f_contiguous)
        self.assertEqual(typeof(arr).layout, 'A')
        self.check_array_flat(arr)
        # Boolean array
        arr = np.bool_([1, 0, 0, 1] * 2).reshape((2, 2, 2))
        self.check_array_flat(arr)

    def test_array_flat_empty(self):
        # Test .flat with various shapes of empty arrays, contiguous
        # and non-contiguous (see issue #846).
        arr = np.zeros(0, dtype=np.int32)
        arr = arr.reshape(0, 2)
        arrty = types.Array(types.int32, 2, layout='C')
        self.check_array_flat_sum(arr, arrty)
        arrty = types.Array(types.int32, 2, layout='F')
        self.check_array_flat_sum(arr, arrty)
        arrty = types.Array(types.int32, 2, layout='A')
        self.check_array_flat_sum(arr, arrty)
        arr = arr.reshape(2, 0)
        arrty = types.Array(types.int32, 2, layout='C')
        self.check_array_flat_sum(arr, arrty)
        arrty = types.Array(types.int32, 2, layout='F')
        self.check_array_flat_sum(arr, arrty)
        arrty = types.Array(types.int32, 2, layout='A')
        self.check_array_flat_sum(arr, arrty)

    def test_array_flat_getitem(self):
        # Test indexing of array.flat object
        pyfunc = array_flat_getitem
        def check(arr, ind):
            cr = self.ccache.compile(pyfunc, (typeof(arr), typeof(ind)))
            expected = pyfunc(arr, ind)
            self.assertEqual(cr.entry_point(arr, ind), expected)

        arr = np.arange(24).reshape(4, 2, 3)
        for i in range(arr.size):
            check(arr, i)
        arr = arr.T
        for i in range(arr.size):
            check(arr, i)
        arr = arr[::2]
        for i in range(arr.size):
            check(arr, i)
        arr = np.array([42]).reshape(())
        for i in range(arr.size):
            check(arr, i)
        # Boolean array
        arr = np.bool_([1, 0, 0, 1])
        for i in range(arr.size):
            check(arr, i)
        arr = arr[::2]
        for i in range(arr.size):
            check(arr, i)

    def test_array_flat_setitem(self):
        # Test indexing of array.flat object
        pyfunc = array_flat_setitem
        def check(arr, ind):
            arrty = typeof(arr)
            cr = self.ccache.compile(pyfunc, (arrty, typeof(ind), arrty.dtype))
            # Use np.copy() to keep the layout
            expected = np.copy(arr)
            got = np.copy(arr)
            pyfunc(expected, ind, 123)
            cr.entry_point(got, ind, 123)
            self.assertPreciseEqual(got, expected)

        arr = np.arange(24).reshape(4, 2, 3)
        for i in range(arr.size):
            check(arr, i)
        arr = arr.T
        for i in range(arr.size):
            check(arr, i)
        arr = arr[::2]
        for i in range(arr.size):
            check(arr, i)
        arr = np.array([42]).reshape(())
        for i in range(arr.size):
            check(arr, i)
        # Boolean array
        arr = np.bool_([1, 0, 0, 1])
        for i in range(arr.size):
            check(arr, i)
        arr = arr[::2]
        for i in range(arr.size):
            check(arr, i)

    def test_array_flat_len(self):
        # Test len(array.flat)
        pyfunc = array_flat_len
        def check(arr):
            cr = self.ccache.compile(pyfunc, (typeof(arr),))
            expected = pyfunc(arr)
            self.assertPreciseEqual(cr.entry_point(arr), expected)

        arr = np.arange(24).reshape(4, 2, 3)
        check(arr)
        arr = arr.T
        check(arr)
        arr = arr[::2]
        check(arr)
        arr = np.array([42]).reshape(())
        check(arr)

    def test_array_flat_premature_free(self):
        cres = compile_isolated(array_flat_premature_free, [types.intp])
        cfunc = cres.entry_point
        expect = array_flat_premature_free(6)
        got = cfunc(6)
        self.assertTrue(got.sum())
        self.assertPreciseEqual(expect, got)

    @tag('important')
    def test_array_ndenumerate_2d(self):
        arr = np.arange(12).reshape(4, 3)
        arrty = typeof(arr)
        self.assertEqual(arrty.ndim, 2)
        self.assertEqual(arrty.layout, 'C')
        self.assertTrue(arr.flags.c_contiguous)
        # Test with C-contiguous array
        self.check_array_ndenumerate_sum(arr, arrty)
        # Test with Fortran-contiguous array
        arr = arr.transpose()
        self.assertFalse(arr.flags.c_contiguous)
        self.assertTrue(arr.flags.f_contiguous)
        arrty = typeof(arr)
        self.assertEqual(arrty.layout, 'F')
        self.check_array_ndenumerate_sum(arr, arrty)
        # Test with non-contiguous array
        arr = arr[::2]
        self.assertFalse(arr.flags.c_contiguous)
        self.assertFalse(arr.flags.f_contiguous)
        arrty = typeof(arr)
        self.assertEqual(arrty.layout, 'A')
        self.check_array_ndenumerate_sum(arr, arrty)
        # Boolean array
        arr = np.bool_([1, 0, 0, 1]).reshape((2, 2))
        self.check_array_ndenumerate_sum(arr, typeof(arr))

    def test_array_ndenumerate_empty(self):
        arr = np.zeros(0, dtype=np.int32)
        arr = arr.reshape(0, 2)
        arrty = types.Array(types.int32, 2, layout='C')
        self.check_array_ndenumerate_sum(arr, arrty)
        arrty = types.Array(types.int32, 2, layout='F')
        self.check_array_ndenumerate_sum(arr, arrty)
        arrty = types.Array(types.int32, 2, layout='A')
        self.check_array_ndenumerate_sum(arr, arrty)
        arr = arr.reshape(2, 0)
        arrty = types.Array(types.int32, 2, layout='C')
        self.check_array_flat_sum(arr, arrty)
        arrty = types.Array(types.int32, 2, layout='F')
        self.check_array_flat_sum(arr, arrty)
        arrty = types.Array(types.int32, 2, layout='A')
        self.check_array_flat_sum(arr, arrty)

    def test_array_ndenumerate_premature_free(self):
        cres = compile_isolated(array_ndenumerate_premature_free, [types.intp])
        cfunc = cres.entry_point
        expect = array_ndenumerate_premature_free(6)
        got = cfunc(6)
        self.assertTrue(got.sum())
        self.assertPreciseEqual(expect, got)

    def test_np_ndindex(self):
        func = np_ndindex
        cres = compile_isolated(func, [types.int32, types.int32])
        cfunc = cres.entry_point
        self.assertPreciseEqual(cfunc(3, 4), func(3, 4))
        self.assertPreciseEqual(cfunc(3, 0), func(3, 0))
        self.assertPreciseEqual(cfunc(0, 3), func(0, 3))
        self.assertPreciseEqual(cfunc(0, 0), func(0, 0))

    @tag('important')
    def test_np_ndindex_array(self):
        func = np_ndindex_array
        arr = np.arange(12, dtype=np.int32) + 10
        self.check_array_unary(arr, typeof(arr), func)
        arr = arr.reshape((4, 3))
        self.check_array_unary(arr, typeof(arr), func)
        arr = arr.reshape((2, 2, 3))
        self.check_array_unary(arr, typeof(arr), func)

    def test_np_ndindex_empty(self):
        func = np_ndindex_empty
        cres = compile_isolated(func, [])
        cfunc = cres.entry_point
        self.assertPreciseEqual(cfunc(), func())

    @tag('important')
    def test_iter_next(self):
        # This also checks memory management with iter() and next()
        func = iter_next
        arr = np.arange(12, dtype=np.int32) + 10
        self.check_array_unary(arr, typeof(arr), func)


class TestNdIter(MemoryLeakMixin, TestCase):
    """
    Test np.nditer()
    """

    def inputs(self):
        # All those inputs are compatible with a (3, 4) main shape

        # scalars
        yield np.float32(100)

        # 0-d arrays
        yield np.array(102, dtype=np.int16)

        # 1-d arrays
        yield np.arange(4).astype(np.complex64)
        yield np.arange(8)[::2]

        # 2-d arrays
        a = np.arange(12).reshape((3, 4))
        yield a
        yield a.copy(order='F')
        a = np.arange(24).reshape((6, 4))[::2]
        yield a

    def basic_inputs(self):
        yield np.arange(4).astype(np.complex64)
        yield np.arange(8)[::2]
        a = np.arange(12).reshape((3, 4))
        yield a
        yield a.copy(order='F')

    def check_result(self, got, expected):
        self.assertEqual(set(got), set(expected), (got, expected))

    def test_nditer1(self):
        pyfunc = np_nditer1
        cfunc = jit(nopython=True)(pyfunc)
        for a in self.inputs():
            expected = pyfunc(a)
            got = cfunc(a)
            self.check_result(got, expected)

    @tag('important')
    def test_nditer2(self):
        pyfunc = np_nditer2
        cfunc = jit(nopython=True)(pyfunc)
        for a, b in itertools.product(self.inputs(), self.inputs()):
            expected = pyfunc(a, b)
            got = cfunc(a, b)
            self.check_result(got, expected)

    def test_nditer3(self):
        pyfunc = np_nditer3
        cfunc = jit(nopython=True)(pyfunc)
        # Use a restricted set of inputs, to shorten test time
        inputs = self.basic_inputs
        for a, b, c in itertools.product(inputs(), inputs(), inputs()):
            expected = pyfunc(a, b, c)
            got = cfunc(a, b, c)
            self.check_result(got, expected)

    def test_errors(self):
        # Incompatible shapes
        pyfunc = np_nditer2
        cfunc = jit(nopython=True)(pyfunc)

        self.disable_leak_check()

        def check_incompatible(a, b):
            with self.assertRaises(ValueError) as raises:
                cfunc(a, b)
            self.assertIn("operands could not be broadcast together",
                          str(raises.exception))

        check_incompatible(np.arange(2), np.arange(3))
        a = np.arange(12).reshape((3, 4))
        b = np.arange(3)
        check_incompatible(a, b)


if __name__ == '__main__':
    unittest.main()
