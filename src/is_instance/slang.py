__all__ = [
    'translate_slang',
]
def translate_slang(obj):
    """
    Slang for the haskell type system.

    Allows using abbreviations like:

    * [int] to stand for list[int]

    * {str: bool} to stand for dict[str, bool]

    * [[int]] to stand for list[list[int]]

    Lets us talk about types in a better way
    without having to actually use haskell.
    """
    if len(obj) != 1:
        raise TypeError(f"Not a valid type schema")
    for cls in (tuple, list, set):
        if isinstance(obj, cls):
            return cls[*obj]
    for cls in (dict,):
        if isinstance(obj, cls):
            [(key, val)] = obj.items()
            return cls[key, val]
    raise TypeError(obj)
