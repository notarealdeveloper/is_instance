#!/usr/bin/env python3

import sys
import types
import typing
from functools import reduce
from operator import or_


def is_instance(obj, cls):

    """
        Turducken typing.

        assert is_instance('spam', str)
        assert is_instance('spam', (str, int))
        assert is_instance(['spam', 'and', 'eggs'], list[str])
        assert is_instance((), tuple[int])
        assert is_instance((1, 2, 3), tuple[int])
        assert is_instance({'bird': True, 'alive': False}, dict[str, bool])
        assert is_instance([{3: int}, {'s': str}], list[dict[object, type]])

        d1 = {'age': 88, 'old': True}
        d2 = {'age': 22, 'old': False}
        assert is_instance([d1, d2], list[dict[str, int | bool]])
        assert is_instance([d1, d2], list[dict[str, int]])
        assert not is_instance([d1, d2], list[dict[str, bool]])
        assert not is_instance([d1, d2], list[dict[str, str]])
    """

    if isinstance(cls, tuple):
        if all(isinstance(sub, type) for sub in cls):
            cls = reduce(or_, cls)
            return is_instance(obj, cls)

    if isinstance(cls, types.UnionType):
        return any(is_instance(obj, sub) for sub in cls.__args__)

    if isinstance(cls, (list, set, dict)):
        cls = from_algebraic_data_type(cls)

    if not isinstance(cls, types.GenericAlias):
        return isinstance(obj, cls)

    if not is_instance(obj, cls.__origin__):
        return False

    outer_type  = cls.__origin__
    inner_types = cls.__args__

    if issubclass(outer_type, (list, tuple, set)):
        assert len(inner_types) == 1
        [inner_type] = inner_types
        return all(is_instance(item, inner_type) for item in obj)

    if issubclass(outer_type, dict):
        assert len(inner_types) == 2
        key_type, val_type = inner_types
        return all(
            is_instance(key, key_type) and
            is_instance(val, val_type) for
            key, val in obj.items()
        )

    raise TypeError(obj, cls)


def from_algebraic_data_type(obj):
    """
    Slang for the haskell type system.

    Allows using abbreviations like:

    * [int] to stand for list[int]

    * {str: bool} to stand for dict[str, bool]

    * [[int]] to stand for list[list[int]]

    Lets us talk about types in a better way
    without having to actually use haskell.
    """
    if len(obj) != 1:
        raise TypeError(f"Not a valid type schema")
    for cls in (tuple, list, set):
        if isinstance(obj, cls):
            return cls[*obj]
    for cls in (dict,):
        if isinstance(obj, cls):
            [(key, val)] = obj.items()
            return cls[key, val]
    raise TypeError(obj)



def test():

    # test_compat
    assert is_instance('spam', str)
    assert is_instance('spam', (str, int))
    assert is_instance(True, int)
    assert not is_instance('spam', int)
    assert not is_instance('spam', (float, int))
    assert not is_instance(True, float)

    # test_nesting
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

    # test_slang
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

    import inspect
    print(inspect.getsource(test), file=sys.stderr)
    print("All tests passed", file=sys.stderr)

is_instance.__test__ = test
is_instance.__type__ = from_algebraic_data_type
sys.modules[__name__] = is_instance

