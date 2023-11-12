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
