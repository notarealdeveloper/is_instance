import is_instance

def test_compat():
    assert is_instance('spam', str)
    assert is_instance('spam', (str, int))
    assert is_instance(True, int)
    assert not is_instance('spam', int)
    assert not is_instance('spam', (float, int))
    assert not is_instance(True, float)

def test_nesting():
    d1 = {'age': 88, 'old': True}
    d2 = {'age': 22, 'old': False}
    assert is_instance(['spam', 'and', 'eggs'], list[str])
    assert is_instance([], list[int])
    assert is_instance({1, 2, 3}, set[int])
    assert is_instance({'bird': True, 'alive': False}, dict[str, bool])
    assert is_instance([{3: int}, {'s': str}], list[dict[object, type]])
    assert is_instance([d1, d2], list[dict[str, int | bool]])
    assert is_instance([d1, d2], list[dict[str, int]])
    assert not is_instance([d1, d2], list[dict[str, bool]])
    assert not is_instance([d1, d2], list[dict[str, str]])

def test_typed_tuples():
    # note: this example does not work in the corresponding slang,
    # since it's impossible to support that behavior without
    # sacrificing the more important goal of matching the builtin
    # isinstance behavior whenever possible. in other words:
    assert is_instance(('cake', 'pie', 42), tuple[str, str, int])

    # make sure we still match builtin isinstance's behavior
    assert not isinstance(('cake', 'pie', 42), (str, str, int))
    assert not is_instance(('cake', 'pie', 42), (str, str, int))

def test_slang():
    d1 = {'age': 88, 'old': True}
    d2 = {'age': 22, 'old': False}
    assert is_instance(['spam', 'and', 'eggs'], [str])
    assert is_instance([], [int])
    assert is_instance({1, 2, 3}, {int})
    assert is_instance({'bird': True, 'alive': False}, {str: bool})
    assert is_instance([{3: int}, {'s': str}], [{object: type}])
    assert is_instance([d1, d2], [{str: int | bool}])
    assert is_instance([d1, d2], [{str: int}])
    assert not is_instance([d1, d2], [{str: bool}])
    assert not is_instance([d1, d2], [{str: str}])


"""
The tests below are a bit excessive, but fun.

Iterate over all objects in the typing module.

If they're classes we can perform a cls[a] on
for single type a, then make sure is_instance
behaves as expected on them.
"""

def test_unary_abcs():

    import types
    import typing
    modules = (types, typing)

    obj = ['cake']

    for module in modules:
        for name, cls in vars(module).items():

            # if we're not looking at a class object, ignore it
            if not isinstance(cls, type):
                continue

            # if we're not looking at a unary abc, ignore it
            try:
                cls[str]
            except:
                continue

            # if we're here, it's a unary abstract base class,
            # so make sure it behaves how we expect it to.
            if issubclass(list, cls):
                assert     is_instance(obj, cls)
                assert     is_instance(obj, cls[str])
                assert not is_instance(obj, cls[int])
            else:
                assert not is_instance(obj, cls)
                assert not is_instance(obj, cls[str])
                assert not is_instance(obj, cls[int])

def test_binary_abcs():

    import types
    import typing
    modules = (types, typing)

    obj = {"cake": "pie"}

    for module in modules:
        for name, cls in vars(module).items():

            # if we're not looking at a class object, ignore it
            if not isinstance(cls, type):
                continue

            # if we're not looking at a binary abc, ignore it
            try:
                cls[str, str]
            except:
                continue

            # if we're here, it's a unary abstract base class,
            # so make sure it behaves how we expect it to.
            if isinstance(obj, cls):
                assert     is_instance(obj, cls)
                assert     is_instance(obj, cls[str, str])
                assert not is_instance(obj, cls[str, int])
                assert not is_instance(obj, cls[int, str])
            else:
                assert not is_instance(obj, cls)
                assert not is_instance(obj, cls[str, str])
                assert not is_instance(obj, cls[str, int])
                assert not is_instance(obj, cls[int, str])
