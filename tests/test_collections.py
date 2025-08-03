# contributed by Michael I Chen <Michael.Chen@aicadium.ai>

import is_instance

from collections.abc import (
    Collection,
    Container,
    Iterable,
    Mapping,
    Reversible,
    Sequence,
)

def test_collection():
    assert is_instance(["cake"], Collection[str])
    assert not is_instance(["cake"], Collection[int])

def test_container():
    assert is_instance(["cake"], Container[str])
    assert not is_instance(["cake"], Container[int])

def test_iterable():
    assert is_instance(["cake"], Iterable[str])
    assert not is_instance(["cake"], Iterable[int])

def test_mapping():
    assert is_instance({"cake": "pie"}, Mapping[str, str])
    assert not is_instance({"cake": "pie"}, Mapping[str, int])

def test_reversible():
    assert is_instance(["cake"], Reversible[str])
    assert not is_instance(["cake"], Reversible[int])

def test_sequence():
    assert is_instance(["cake"], Sequence[str])
    assert not is_instance(["cake"], Sequence[int])
