# Contents in this file are referenced from the sphinx-generated docs.
# "magictoken" is used for markers as beginning and ending of example text.


def ex_typed_dict_from_cpython():
    # magictoken.ex_typed_dict_from_cpython.begin
    import numpy as np
    from numba import njit
    from numba import types
    from numba.typed import Dict

    # The Dict.empty() constructs a typed dictionary.
    # The key and value typed must be explicitly declared.
    d = Dict.empty(
        key_type=types.unicode_type,
        value_type=types.float64[:],
    )

    # The typed-dict can be used from the interpreter.
    d['posx'] = np.asarray([1, 0.5, 2], dtype='f8')
    d['posy'] = np.asarray([1.5, 3.5, 2], dtype='f8')
    d['velx'] = np.asarray([0.5, 0, 0.7], dtype='f8')
    d['vely'] = np.asarray([0.2, -0.2, 0.1], dtype='f8')

    # Here's a function that expects a typed-dict as the argument
    @njit
    def move(d):
        # inplace operations on the arrays
        d['posx'] += d['velx']
        d['posy'] += d['vely']

    print('posx: ', d['posx'])  # Out: posx:  [1.  0.5 2. ]
    print('posy: ', d['posy'])  # Out: posy:  [1.5 3.5 2. ]

    # Call move(d) to inplace update the arrays in the typed-dict.
    move(d)

    print('posx: ', d['posx'])  # Out: posx:  [1.5 0.5 2.7]
    print('posy: ', d['posy'])  # Out: posy:  [1.7 3.3 2.1]
    # magictoken.ex_typed_dict_from_cpython.end

    # Test
    np.testing.assert_array_equal(d['posx'], [1.5, 0.5, 2.7])
    np.testing.assert_array_equal(d['posy'], [1.7, 3.3, 2.1])


def ex_typed_dict_njit():
    # magictoken.ex_typed_dict_njit.begin
    import numpy as np
    from numba import njit
    from numba import types
    from numba.typed import Dict

    # Make array type.  Type-expression is not supported in jit functions.
    float_array = types.float64[:]

    @njit
    def foo():
        # Make dictionary
        d = Dict.empty(
            key_type=types.unicode_type,
            value_type=float_array,
        )
        # Fill the dictionary
        d["posx"] = np.arange(3).astype(np.float64)
        d["posy"] = np.arange(3, 6).astype(np.float64)
        return d

    d = foo()
    # Print the dictionary
    print(d)  # Out: {posx: [0. 1. 2.], posy: [3. 4. 5.]}
    # magictoken.ex_typed_dict_njit.end
    np.testing.assert_array_equal(d['posx'], [0, 1, 2])
    np.testing.assert_array_equal(d['posy'], [3, 4, 5])
