# is_instance

A better isinstance for python.

## examples

```python3
import is_instance

>>> is_instance(['spam', 'and', 'eggs'], list[str])
True

>>> is_instance(['spam', 'and', 'eggs'], list[int])
False

>>> is_instance({'bird': True, 'alive': False}, dict[str, bool])
True

>>> is_instance({(),(1,2),(4,5,'6')}, set[tuple[int]])
False

>>> is_instance({(),(1,2),(4,5,6)}, set[tuple[int]])
True

>>> is_instance([{'a': 1, 'b': None}, {'a': 3, 'b': 4}], list[dict[str, int]])
False

>>> is_instance([{'a': 1, 'b': None}, {'a': 3, 'b': 4}], list[dict[str, int|None]])
True
```

The following type slang is also supported, inspired by the Haskell type system.

```python3
import is_instance

>>> is_instance(['spam', 'and', 'eggs'], [str])
True

>>> is_instance(['spam', 'and', 'eggs'], [int])
False

>>> is_instance({'bird': True, 'alive': False}, {str: bool})
True

>>> is_instance([{'a': 1, 'b': None}, {'a': 3, 'b': 4}], [{str: int}])
False

>>> is_instance([{'a': 1, 'b': None}, {'a': 3, 'b': 4}], [{str: int | None}])
True
```
