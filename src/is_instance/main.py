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

    cls_origin = typing.get_origin(cls)
    cls_args   = typing.get_args(cls)

    if isinstance(cls, typing._LiteralGenericAlias):
        return obj in cls_args

    if not is_instance(obj, cls_origin):
        return False

    if issubclass(cls_origin, tuple):
        if len(cls_args) != len(obj):
            return False
        return all(is_instance(item, cls_arg) for item, cls_arg in zip(obj, cls_args))

    if issubclass(cls_origin, Mapping):
        assert len(cls_args) == 2
        key_type, val_type = cls_args
        return all(
            is_instance(key, key_type) and
            is_instance(val, val_type) for
            key, val in obj.items()
        )

    if issubclass(cls_origin, (Container, Sequence)):
        assert len(cls_args) == 1, cls
        [cls_arg] = cls_args
        return all(is_instance(item, cls_arg) for item in obj)

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
