from collections.abc import (
    Callable,
    Collection,
    Container,
    Generator,
    Iterable,
    Iterator,
    Mapping,
    MutableMapping,
    MutableSequence,
    MutableSet,
    Reversible,
    Sequence,
    Set,
)
from types import MappingProxyType
from typing import Literal

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
    assert is_instance(None, None)
    assert is_instance([], [int])
    assert is_instance({1, 2, 3}, {int})
    assert is_instance({'bird': True, 'alive': False}, {str: bool})
    assert is_instance([{3: int}, {'s': str}], [{object: type}])
    assert is_instance([d1, d2], [{str: int | bool}])
    assert is_instance([d1, d2], [{str: int}])
    assert not is_instance([d1, d2], [{str: bool}])
    assert not is_instance([d1, d2], [{str: str}])

def test_literal():
    assert is_instance('', Literal[''])
    assert is_instance('', Literal['', 0])
    assert is_instance('', Literal[Literal['']])
    assert not is_instance(Literal[''], Literal[Literal['']])
    assert not is_instance('', Literal[0])

def test_collection():
    assert is_instance('', Collection[str])
    assert is_instance('', Collection[Collection[str]])
    assert not is_instance('', Collection[int])
    assert not is_instance(0, Collection)

def test_container():
    assert is_instance('', Container[str])
    assert is_instance('', Container[Container[str]])
    assert not is_instance('', Container[int])
    assert not is_instance(0, Container)

def test_iterable():
    assert is_instance('', Iterable[str])
    assert is_instance('', Iterable[Iterable[str]])
    assert not is_instance('', Iterable[int])
    assert not is_instance(0, Iterable)

def test_mapping():
    assert is_instance({'': ''}, Mapping[str, str])
    assert not is_instance({'': ''}, Mapping[str, int])
    assert not is_instance('', Mapping)

def test_mutable_mapping():
    assert is_instance({'': ''}, MutableMapping[str, str])
    assert not is_instance({'': ''}, MutableMapping[str, int])
    assert not is_instance(MappingProxyType({}), MutableMapping)

def test_reversible():
    assert is_instance('', Reversible[str])
    assert is_instance('', Reversible[Reversible[str]])
    assert not is_instance('', Reversible[int])
    assert not is_instance(set(), Reversible)

def test_sequence():
    assert is_instance('', Sequence[str])
    assert is_instance('', Sequence[Sequence[str]])
    assert not is_instance('', Sequence[int])
    assert not is_instance(set(), Sequence)

def test_mutable_sequence():
    assert is_instance([''], MutableSequence[str])
    assert is_instance([[]], MutableSequence[MutableSequence[None]])
    assert not is_instance([''], MutableSequence[int])
    assert not is_instance('', MutableSequence)

def test_set():
    assert is_instance({''}, Set[str])
    assert is_instance({frozenset()}, Set[Set[None]])
    assert not is_instance({''}, Set[int])
    assert not is_instance([], Set)

def test_mutable_set():
    assert is_instance({''}, MutableSet[str])
    assert not is_instance({''}, MutableSet[int])
    assert not is_instance(frozenset(), MutableSet)

############
### TODO ###
############

def TODO_test_typed_tuples_ellipsis():
    assert is_instance((), tuple[int, ...])
    assert is_instance((1,), tuple[int, ...])
    assert is_instance((1, 2), tuple[int, ...])

def TODO_test_callable():
    assert not is_instance(lambda: None, Callable[[str], None])
    assert is_instance(lambda: None, Callable[[], None])
    def fun(x: str) -> None: ...
    assert is_instance(fun, Callable[[str], None])
    def fun(x: str, y: int) -> None: ...
    assert is_instance(fun, Callable[[str, int], None])
    def fun(x: None) -> str: ...
    assert is_instance(fun, Callable[[None], str])

def TODO_test_generator():
    assert is_instance((_ for _ in ''), Generator[str, None, None])
    assert not is_instance((_ for _ in ''), Generator[int, None, None])
    # TODO: test Generator[...] + send/receive

def TODO_test_iterator():
    assert is_instance(iter(''), Iterator[str])
    assert is_instance(iter(iter('')), Iterator[Iterator[str]])
    assert not is_instance(iter(''), Iterator[int])
    assert not is_instance('', Iterator)
