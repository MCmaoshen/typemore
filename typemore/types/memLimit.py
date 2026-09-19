import functools
from typing import Literal
from pympler import asizeof
from .._PackageTools import private

class MemLimitError(MemoryError):
    pass

_MUTATING_METHODS = {
    "append", "extend", "insert", "pop", "remove", "clear",
    "add", "discard", "update", "popitem", "setdefault",
    "sort", "reverse",
    "difference_update", "intersection_update",
    "symmetric_difference_update",
}

_MUTATING_MAGICS = {
    "__setitem__", "__delitem__",
    "__iadd__", "__imul__", "__ior__", "__iand__",
    "__isub__", "__ixor__",
}

_IMMUTABLE = (tuple, str, bytes, frozenset)

def _collect_magics(base):
    names = set()
    for klass in base.__mro__:
        for name in vars(klass):
            if name.startswith("__") and name.endswith("__"):
                names.add(name)
    return names & _MUTATING_MAGICS

def _make_magic_wrapper(name):
    def wrapper(self, *args, **kwargs):
        result = getattr(super(type(self), self), name)(*args, **kwargs)
        MemLimit._check(self)
        return result
    wrapper.__name__ = name
    return wrapper

class MemLimit:
    """A wrapper that enforces a maximum memory size on a container.

        MemLimit wraps a container and checks its total memory size after any
        operation that could change it. If the size exceeds the limit,
        MemLimitError is raised. The size is measured by pympler.asizeof, which
        includes the container and the objects it references.

        The limit is fixed at construction time. The unit argument accepts 'B',
        'KiB', 'MiB', or 'GiB', and defaults to 'B'. The limit is stored
        internally in bytes.

        Example:
            >>> lst = MemLimit([1, 2, 3], 1, 'KiB')
            >>> lst.append(4)
            >>> lst.append(b"x" * 2000)
            MemLimitError: memory limit exceeded: ... > 1024
        """
    _cache = {}

    def __new__(cls, value, limit: int | float, unit: Literal['B', 'KiB', 'MiB', 'GiB'] = 'B'):
        if not isinstance(limit, int | float):
            raise TypeError(f"memory limit must be an int(bytes), not {type(limit).__name__!r}")
        base = type(value)
        if base not in cls._cache:
            magics = _collect_magics(base)
            namespace = {name: _make_magic_wrapper(name) for name in magics}
            cls._cache[base] = type(
                f"MemLimit[{base.__name__}]",
                (cls, base),
                namespace,
            )
        new_cls = cls._cache[base]

        if issubclass(base, _IMMUTABLE):
            return base.__new__(new_cls, value)
        return base.__new__(new_cls)

    def __init__(self, value, limit, unit: Literal['B', 'KiB', 'MiB', 'GiB'] = 'B'):
        object.__setattr__(self, "_limit", 0)          # 先占位
        object.__setattr__(self, "_checking", False)

        if unit == 'B':
            limit_bytes = limit
        elif unit == 'KiB':
            limit_bytes = limit * 1024
        elif unit == 'MiB':
            limit_bytes = limit * 1048576
        elif unit == 'GiB':
            limit_bytes = limit * 1073741824
        else:
            raise ValueError(f"unknown unit: {unit!r}")
        object.__setattr__(self, "_limit", limit_bytes)

        if isinstance(self, _IMMUTABLE):
            self._check()
            return

        self._fill(value)
        self._check()

    @private
    def _fill(self, value):
        base = self._find_base()
        if base is not None:
            try:
                base.__init__(self, value)
                return
            except TypeError:
                pass
        for name in ("update", "extend"):
            method = getattr(super(type(self), self), name, None)
            if method is not None:
                try:
                    method(value)
                    return
                except TypeError:
                    pass
        for name in ("append", "add"):
            method = getattr(super(type(self), self), name, None)
            if method is not None:
                for item in value:
                    method(item)
                return
        raise TypeError(
            f"cannot fill {type(self).__name__} from {type(value).__name__!r}"
        )

    @private
    def _find_base(self):
        for klass in type(self).__mro__:
            if klass is not MemLimit and klass is not object and not issubclass(klass, MemLimit):
                return klass
        return None

    @private
    def _check(self):
        if getattr(self, "_checking", False):
            return
        object.__setattr__(self, "_checking", True)
        try:
            current = asizeof.asizeof(self)
            if current > self._limit:
                raise MemLimitError(
                    f"memory limit exceeded: {current} > {self._limit}"
                )
        finally:
            object.__setattr__(self, "_checking", False)

    def __getattr__(self, name):
        if name.startswith("_"):
            raise AttributeError(name)
        attr = getattr(super(type(self), self), name)
        if callable(attr) and name in _MUTATING_METHODS:
            @functools.wraps(attr)
            def wrapper(*args, **kwargs):
                result = attr(*args, **kwargs)
                MemLimit._check(self)
                return result
            return wrapper
        return attr

    def __str__(self):
        return super().__str__()

    def __repr__(self):
        return f"MemLimit({super().__repr__()}, limit={self._limit})"