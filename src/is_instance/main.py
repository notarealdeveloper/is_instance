__all__ = [
    'is_instance',
]

import sys
import types
import typing
from collections import deque
from collections.abc import Callable, Container, Generator, Iterable, Iterator, Mapping
from itertools import groupby


def is_instance(obj, cls, /):

    """ Turducken typing. """

    if isinstance(cls, tuple):
        return any(is_instance(obj, sub) for sub in cls)

    if sys.version_info >= (3,10) and isinstance(cls, types.UnionType):
        return any(is_instance(obj, sub) for sub in cls.__args__)

    if isinstance(cls, (list, set, dict)):
        cls = translate_slang(cls)

    if cls is None:
        cls = types.NoneType

    if sys.version_info >= (3, 6, 2):
        if cls == typing.NoReturn:
            return False
        if sys.version_info >= (3, 11):
            if cls == typing.Never:
                return False

    if not isinstance(cls, (types.GenericAlias, typing._GenericAlias)):
        return isinstance(obj, cls)

    cls_origin = typing.get_origin(cls)
    cls_args   = typing.get_args(cls)

    if isinstance(cls, typing._LiteralGenericAlias):
        return obj in cls_args

    if not is_instance(obj, cls_origin):
        return False

    if issubclass(cls_origin, tuple):
        if Ellipsis in cls_args:
            return _ellipsis(obj, cls_args)
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

    if issubclass(cls_origin, Generator):
        raise NotImplementedError('Generator not yet supported')

    if issubclass(cls_origin, Iterator):
        raise NotImplementedError('Iterator not yet supported')

    if issubclass(cls_origin, (Container, Iterable)):
        assert len(cls_args) == 1
        [inner_type] = cls_args
        if len(obj):
            return all(is_instance(item, inner_type) for item in obj)
        return is_instance(obj, inner_type) or hasattr(obj, '__class_getitem__')

    if issubclass(cls_origin, Callable):
        raise NotImplementedError('Callable not yet supported')

    raise TypeError(obj, cls)


def _ellipsis(objs, types_, /) -> bool:
    """Check if objs is a valid ordering according to types in the subscript."""
    objs, types_ = deque(objs), deque(types_)

    # trim initial/terminal non-Ellipsis
    for idx in (0, -1):
        pop_side = f"pop{'left' * (idx + 1)}"
        pop_objs, pop_types = getattr(objs, pop_side), getattr(types_, pop_side)
        while types_ and types_[idx] is not Ellipsis:
            if objs and is_instance(pop_objs(), pop_types()):
                continue
            return False
    assert types_[0] is Ellipsis and types_[-1] is Ellipsis

    pop_objs = objs.popleft
    for current_types in (  # split remaining types on Ellipsis into consecutive groups
        deque(group)  # incidentally, this collapses consecutive Ellipsis args
        for key, group in groupby(types_, lambda typ: typ is Ellipsis)
        if not key
    ):
        pop_types = current_types.popleft
        while current_types:
            if objs:
                if is_instance(pop_objs(), current_types[0]):
                    pop_types()
                continue
            return False

    return True


if sys.version_info >= (3, 11):
    # translate_slang needs to write cls[*obj],
    # which is apparently a syntax error in older
    # versions of python, so we shouldn't even
    # import the .slang module unless we're running
    # at least python 3.11
    from .slang import translate_slang
else:
    translate_slang = lambda x: x
