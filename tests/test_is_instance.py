from collections.abc import (
    Callable,
    Collection,
    Container,
    Generator,
    Iterable,
    Iterator,
    Mapping,
    Reversible,
    Sequence,
)

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

def test_collection():
    assert is_instance('', Collection[str])
    assert not is_instance('', Collection[int])
    assert not is_instance(0, Collection)

def test_container():
    assert is_instance('', Container[str])
    assert not is_instance('', Container[int])
    assert not is_instance(0, Container)

def test_iterable():
    assert is_instance('', Iterable[str])
    assert not is_instance('', Iterable[int])
    assert not is_instance(0, Iterable)

def test_iterator():
    assert is_instance(iter(''), Iterator[str])
    assert not is_instance(iter(''), Iterator[int])
    assert not is_instance('', Iterator)

def test_mapping():
    assert is_instance({'': 0}, Mapping[str, int])
    assert not is_instance({'': ''}, Mapping[str, int])
    assert not is_instance('', Mapping)

def test_reversible():
    assert is_instance('', Reversible[str])
    assert not is_instance('', Reversible[int])
    assert not is_instance(set(), Reversible)

def test_sequence():
    assert is_instance('', Sequence[str])
    assert not is_instance('', Sequence[int])
    assert not is_instance(set(), Sequence)

############
### TODO ###
############

def TODO_test_callable():
    assert not is_instance(lambda: None, Callable[[str], None])
    assert is_instance(lambda: None, Callable[[], None])
    def fun(x: str) -> None: ...
    assert is_instance(fun, Callable[[str], None])
    def fun(x: str, y: int) -> None: ...
    assert is_instance(fun, Callable[[str, int], None])
    def fun(x: str, y: int) -> bool: ...
    assert is_instance(fun, Callable[[str, int], bool])

def TODO_test_typed_tuples_ellipsis():
    assert is_instance((), tuple[int, ...])
    assert is_instance((1,), tuple[int, ...])
    assert is_instance((1, 2), tuple[int, ...])

def TODO_test_generator():
    assert is_instance((_ for _ in ''), Generator[str, None, None])
    assert not is_instance((_ for _ in ''), Generator[int, None, None])
    # TODO: test Generator[...] + send/receive
