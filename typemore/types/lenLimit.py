from .._PackageTools import private

class LenLimitError(ValueError):
    pass

_SKIP = {
    "__init__", "__new__", "__setattr__", "__delattr__",
    "__getattribute__", "__get__", "__set__", "__delete__",
    "__dict__", "__weakref__", "__slots__", "__class__",
    "__repr__"
}

_EXCLUDED = (str, bytes, bytearray, memoryview)

@private
def _is_container(value):
    if isinstance(value, _EXCLUDED):
        return False
    if not hasattr(value, "__len__"):
        return False
    if not (hasattr(value, "__iter__") or hasattr(value, "__getitem__")):
        return False
    return True

@private
def _collect_magics(base):
    names = set()
    for klass in base.__mro__:
        for name in vars(klass):
            if name.startswith("__") and name.endswith("__"):
                names.add(name)
    return names

@private
def _make_forward(name):
    def forward(self, *args, **kwargs):
        result = getattr(self._value, name)(*args, **kwargs)
        if len(self._value) > self._limit:
            raise LenLimitError(
                f"length limit exceeded: fixed length is {self._limit}"
            )
        return result
    forward.__name__ = name
    return forward

class LenLimit:
    """A wrapper that enforces a maximum length on a container.

        LenLimit wraps a container such as a list, dict, or set. After any
        operation that could change its length, the wrapper checks the real
        length and raises LenLimitError if it exceeds the limit. The limit is
        fixed at construction time and cannot be changed.

        The wrapper forwards operations to the wrapped container and returns
        plain results, not wrapped ones.

        Example:
            >>> lst = LenLimit([1, 2], 3)
            >>> lst.append(3)
            >>> lst.append(4)
            LenLimitError: length limit exceeded: fixed length is 3
            >>> len(lst)
            3
        """
    _cache = {}

    def __new__(cls, value, limit):
        base = type(value)
        if base not in cls._cache:
            magics = _collect_magics(base) - _SKIP
            namespace = {name: _make_forward(name) for name in magics}
            cls._cache[base] = type(
                f"LenLimit[{base.__name__}]",
                (cls,),
                namespace,
            )
        return object.__new__(cls._cache[base])

    def __init__(self, value, limit: int | float):
        if not isinstance(limit, int | float):
            raise TypeError(f"len limit must be an int or float, not {type(limit).__name__!r}")
        if not _is_container(value):
            raise TypeError(
                f"value must be a container that can hold elements, "
                f"not {type(value).__name__!r}"
            )
        if len(value) > limit:
            raise LenLimitError(
                f"length limit exceeded: {len(value)} > {limit}"
            )
        object.__setattr__(self, "_value", value)
        object.__setattr__(self, "_limit", limit)

    def __getattr__(self, name):
        def forward(*args, **kwargs):
            result = getattr(self._value, name)(*args, **kwargs)
            if len(self._value) > self._limit:
                raise LenLimitError(
                    f"length limit exceeded: fixed length is {self._limit}"
                )
            return result
        return forward

    def __repr__(self):
        return f"({self}, limit={self._limit!r})"