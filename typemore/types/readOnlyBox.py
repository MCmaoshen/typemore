import copy

class ReadOnlyBox:
    """A read-only wrapper that stores a deep copy of a value.

        The wrapped value must be a container that copy.deepcopy can handle.
        Common containers such as list, dict, and set work. Objects that hold
        system resources, such as open files, locks, sockets, and iterators,
        cannot be deep-copied and will raise during construction.

        The copy is deep, so mutable values inside the wrapped object are copied
        too. Later changes to the original do not affect the box, and vice versa.

        Attribute assignment and deletion are blocked; reads are forwarded to
        the wrapped value.

        Example:
            >>> data = [1, 2, 3]
            >>> box = ReadOnlyBox(data)
            >>> data.append(4)
            >>> box.value
            [1, 2, 3]
            >>> box.value = [9]
            AttributeError: can't set attribute 'value'
        """
    __slots__ = ('value',)
    _cache = {}

    def __new__(cls, value):
        base = type(value)
        if base not in cls._cache:
            cls._cache[base] = type(
                f"{cls.__name__}[{base.__name__}]",
                (cls,),
                {}
            )
        new_cls = cls._cache[base]
        instance = super().__new__(new_cls)
        return instance

    def __init__(self, value):
        object.__setattr__(self, "value", copy.deepcopy(value))

    def __str__(self):
        return f"{self.value}"

    def __repr__(self):
        return f"ReadOnlyBox[{type(self.value).__name__}]:{self.value!r}"

    def __getattr__(self, name):
        if name == 'value':
            raise AttributeError(name)
        if hasattr(self.value, name):
            attr = getattr(self.value, name)
            if callable(attr):
                def wrapper(*args, **kwargs):
                    return attr(*args, **kwargs)
                return wrapper
            return attr
        raise AttributeError(f"'{type(self).__name__}' object has no attribute '{name}'")

    def __setattr__(self, name, value):
        raise AttributeError(f"can't set attribute '{name}'")

    def __delattr__(self, name):
        raise AttributeError(f"can't delete attribute '{name}'")