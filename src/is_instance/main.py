__all__ = [
    'is_instance',
    'translate_slang',
]

import types
from functools import reduce
from operator import or_

def is_instance(obj, cls):

    """ Turducken typing. """

    if isinstance(cls, tuple):
        if all(isinstance(sub, type) for sub in cls):
            cls = reduce(or_, cls)
            return is_instance(obj, cls)

    if isinstance(cls, types.UnionType):
        return any(is_instance(obj, sub) for sub in cls.__args__)

    if isinstance(cls, (list, set, dict)):
        cls = translate_slang(cls)

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


def translate_slang(obj):
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
