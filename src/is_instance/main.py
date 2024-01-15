__all__ = [
    'is_instance',
]

import sys
import types
import typing
from collections.abc import Container, Iterable, Mapping, Sequence
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

    if not isinstance(cls, (types.GenericAlias, typing._GenericAlias)):
        return isinstance(obj, cls)

    if not is_instance(obj, cls.__origin__):
        return False

    outer_type  = cls.__origin__
    inner_types = typing.get_args(cls)

    if issubclass(outer_type, tuple):
        if Ellipsis in inner_types:
            raise NotImplementedError("Ellipsis not yet supported")
        if len(inner_types) != len(obj):
            return False
        return all(is_instance(item, inner_type) for item, inner_type in zip(obj, inner_types))

    if issubclass(outer_type, Mapping):
        assert len(inner_types) == 2
        key_type, val_type = inner_types
        return all(
            is_instance(key, key_type) and
            is_instance(val, val_type) for
            key, val in obj.items()
        )

    if issubclass(outer_type, (list, set, Container, Iterable, Sequence)):
        assert len(inner_types) == 1
        [inner_type] = inner_types
        return all(is_instance(item, inner_type) for item in obj)

    if issubclass(outer_type, Callable):
        raise NotImplementedError("Callable not yet supported")

    if issubclass(outer_type, Generator):
        raise NotImplementedError("Generator not yet supported")

    raise TypeError(obj, cls)


if sys.version >= '3.11':
    # translate_slang needs to write cls[*obj],
    # which is apparently a syntax error in older
    # versions of python, so we shouldn't even
    # import the .slang module unless we're running
    # at least python 3.11
    from .slang import translate_slang
else:
    translate_slang = lambda x: x
