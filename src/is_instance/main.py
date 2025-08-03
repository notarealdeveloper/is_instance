__all__ = [
    'is_instance',
]

import sys
import types
import typing
from collections.abc import Container, Iterable, Mapping


def is_instance(obj, cls):

    """
        Turducken typing.¹
    """

    if isinstance(cls, tuple):
        return any(is_instance(obj, sub) for sub in cls)

    if sys.version_info >= (3, 10) and isinstance(cls, types.UnionType):
        return any(is_instance(obj, sub) for sub in cls.__args__)

    if isinstance(cls, (list, set, dict)):
        cls = translate_slang(cls)

    if cls is None:
        cls = types.NoneType

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

    if issubclass(cls_origin, (Container, Iterable)):
        assert len(cls_args) == 1
        [inner_type] = cls_args
        if len(obj):
            return all(is_instance(item, inner_type) for item in obj)
        return is_instance(obj, inner_type) or hasattr(obj, '__class_getitem__')

    raise TypeError(obj, cls)

    """
        Footnote 1: For more details, see the following:
        * https://docs.python.org/3/glossary.html#term-duck-typing
        * https://en.wikipedia.org/wiki/Turducken
        * https://github.com/notarealdeveloper/is_instance/blob/master/src/is_instance/main.py#L73-L78
    """

if sys.version_info >= (3, 11):
    # translate_slang needs to write cls[*obj],
    # which is apparently a syntax error in older
    # versions of python, so we shouldn't even
    # import the .slang module unless we're running
    # at least python 3.11
    from .slang import translate_slang
else:
    translate_slang = lambda x: x
