class Auto:
    """
    This class is compatible with most commonly used type-conversion functions.
    It prevents exceptions for conversion operations that would normally raise them.
    """
    _cache = {}
    _hash = None

    def __new__(cls, auto):
        base = type(auto)
        if base not in cls._cache:
            if base in (bool, type(None)):
                bases = (cls,)
            else:
                bases = (cls, base)
            cls._cache[base] = type(
                f"{cls.__name__}[{base.__name__}]",
                bases,
                {}
            )
        new_cls = cls._cache[base]

        if auto is None or base is bool:
            instance = super().__new__(new_cls)
        elif issubclass(base, (int, float, complex, str, tuple, frozenset, bytes)):
            instance = base.__new__(new_cls, auto)
        elif issubclass(base, (list, dict, set, bytearray)):
            instance = base.__new__(new_cls)
            base.__init__(instance, auto)
        else:
            instance = base.__new__(new_cls)
        return instance

    def __init__(self, auto):
        self.auto = self
        self._hash = None
        try:
            hash(auto)
            self._hash = True
        except TypeError:
            self._hash = False

    def __repr__(self):
        return f"{self.__class__.__name__}:{super().__repr__()}"

    def __getattr__(self, name):
        raise AttributeError(name)

    def __dir__(self):
        return list(set(dir(self.__class__) + dir(self.__class__.__mro__[1]) + ['auto']))

    def __int__(self):
        if not self._hash:
            return len(self)
        if isinstance(self, bool):
            return 1 if bool.__bool__(self) else 0
        if isinstance(self, int):
            return int.__int__(self)
        if isinstance(self, float):
            return int(float.__int__(self))
        if isinstance(self, complex):
            return int(self.real)
        if isinstance(self, str):
            try:
                return int(str.__str__(self))
            except ValueError:
                return 1 if str.__len__(self) else 0
        return 0

    def __float__(self) -> float:
        return float(self.__int__())

    def __complex__(self) -> complex:
        if self._hash:
            if isinstance(self.auto, complex):
                return complex(self.real, self.imag)
            elif isinstance(self.auto, int | float):
                return complex(self.auto, 0j)
            elif isinstance(self.auto, bool):
                if self.auto:
                    real = 1
                else:
                    real = 0
                return complex(real, 0j)
            elif isinstance(self.auto, str):
                try:
                    return complex(self.auto)
                except ValueError:
                    if self.auto.strip() == '':
                        return 0
                    else:
                        return 1
            return complex(0)
        else:
            return complex(self.__int__(), 0j)

    def __index__(self) -> int:
        if self._hash:
            if isinstance(self.auto, int | float | bool):
                return int(self.auto)
            elif isinstance(self.auto, str):
                try:
                    return int(self.auto)
                except ValueError:
                    if self.auto.strip() == '':
                        return 0
                    else:
                        return 1
            elif isinstance(self.auto, complex):
                return int(self.auto.real)
            return 0
        else:
            return self.__int__()

    def __iter__(self):
        auto = self.auto
        if isinstance(auto, (int, float, complex, bool, bytes)):
            return iter([auto])
        return iter(auto)