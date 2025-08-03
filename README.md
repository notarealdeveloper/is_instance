# is_instance

A better isinstance for python.


## usage

```python
>>> import is_instance

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

>>> from collections.abc import Sequence

>>> is_instance('cake', Sequence[str])
True
```

## slang

The following type slang is also supported, inspired by the Haskell type system.

```python
>>> import is_instance

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

## install

To install the package and all required dependencies, run

```
make install
```


## contributing

To get the developer dependencies and a [PEP 660](https://peps.python.org/pep-0660/) editable install, run

```
make develop
```

Once you've made some changes, run

```
make check
```

to see if everything still works.
