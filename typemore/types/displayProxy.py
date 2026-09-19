class DisplayNone:
    def __repr__(self):
        return "DisplayNone"

class RealNone:
    def __repr__(self):
        return "RealNone"

display_none = DisplayNone()
real_none = RealNone()

class DisplayProxyMeta(type):

    def __new__(cls, name, bases, attrs):
        new_class = super().__new__(cls, name, bases, attrs)

        for method_name in new_class.DISPLAY:
            if not hasattr(new_class, method_name):
                setattr(new_class, method_name,
                        cls._make_display_proxy(method_name))

        for method_name in new_class.REAL:
            if not hasattr(new_class, method_name):
                setattr(new_class, method_name,
                        cls._make_real_proxy(method_name))

        return new_class

    @staticmethod
    def _unwrap_args(args, kwargs):
        new_args = []
        for arg in args:
            if isinstance(arg, DisplayProxy):
                if arg._real is not real_none:
                    new_args.append(arg._real)
                elif arg._display is not display_none:
                    new_args.append(arg._display)
                else:
                    new_args.append(arg)
            else:
                new_args.append(arg)

        new_kwargs = {}
        for key, value in kwargs.items():
            if isinstance(value, DisplayProxy):
                if value._real is not real_none:
                    new_kwargs[key] = value._real
                elif value._display is not display_none:
                    new_kwargs[key] = value._display
                else:
                    new_kwargs[key] = value
            else:
                new_kwargs[key] = value

        return new_args, new_kwargs

    @staticmethod
    def _make_display_proxy(name):
        def method(self, *args, **kwargs):
            if self._display is display_none:
                raise AttributeError("object has no attribute: 'display'")
            attr = getattr(self._display, name)
            return attr(*args, **kwargs)

        method.__name__ = name
        return method

    @staticmethod
    def _make_real_proxy(name):
        def method(self, *args, **kwargs):
            if self._real is real_none:
                raise AttributeError("object has no attribute: 'real'")

            if name == '__bool__':
                if hasattr(self._real, '__bool__'):
                    attr = getattr(self._real, '__bool__')
                    return attr(*args, **kwargs)
                if hasattr(self._real, '__len__'):
                    return len(self._real) != 0
                return True

            attr = getattr(self._real, name)
            result = attr(*args, **kwargs)
            if isinstance(result, type(self._real)):
                return DisplayProxy(self._display, result)
            return result

        method.__name__ = name
        return method

class DisplayProxy(metaclass=DisplayProxyMeta):
    """A two-faced proxy that separates display behavior from real behavior.

        A DisplayProxy wraps up to two objects: a display object and a real
        object. Methods and operators are routed to one side depending on their
        name. Display methods such as __str__, __len__, and __getitem__ go to
        the display object; arithmetic, comparison, and conversion methods such
        as __add__, __eq__, and __int__ go to the real object. Names that appear
        in neither list are looked up on the real object first, then on the
        display object.

        When a real-side method returns a value whose type matches the wrapped
        real object, the result is wrapped in a new DisplayProxy so that the
        display behavior is preserved across chained operations.

        Neither side is copied. Modifying a wrapped object affects the original,
        and vice versa.

        Example:
            >>> p = DisplayProxy(display=[1, 2, 3], real=5)
            >>> len(p)          # goes to display
            3
            >>> p + 1           # goes to real
            6
        """
    DISPLAY = (
        '__str__', '__repr__', '__format__',
        '__len__', '__contains__', '__getitem__', '__iter__',
        '__next__',
        '__dir__', '__sizeof__',
        '__setitem__', '__delitem__',
        '__reversed__'
    )

    REAL = (
        '__add__', '__radd__', '__iadd__',
        '__sub__', '__rsub__', '__isub__',
        '__mul__', '__rmul__', '__imul__',
        '__truediv__', '__rtruediv__', '__itruediv__',
        '__floordiv__', '__rfloordiv__', '__ifloordiv__',
        '__mod__', '__rmod__', '__imod__',
        '__pow__', '__rpow__', '__ipow__',
        '__matmul__', '__rmatmul__', '__imatmul__',
        '__lshift__', '__rlshift__', '__ilshift__',
        '__rshift__', '__rrshift__', '__irshift__',
        '__and__', '__rand__', '__iand__',
        '__or__', '__ror__', '__ior__',
        '__xor__', '__rxor__', '__ixor__',
        '__neg__', '__pos__', '__abs__', '__invert__',
        '__lt__', '__le__', '__eq__', '__ne__', '__gt__', '__ge__',
        '__int__', '__float__', '__complex__', '__index__',
        '__trunc__', '__floor__', '__ceil__', '__round__',
        '__hash__',
        '__bool__', '__nonzero__',
        'append', 'extend', 'insert', 'pop', 'remove', 'clear',
        'update', 'setdefault', 'add', 'discard',
        'sort', 'reverse'
    )

    PASSTHROUGH = (
        '__new__', '__init__', '__del__',
        '__getattribute__', '__setattr__', '__delattr__',
        '__get__', '__set__', '__delete__',
        '__await__', '__aiter__', '__anext__',
        '__aenter__', '__aexit__',
        '__enter__', '__exit__',
        '__call__',
        '__instancecheck__', '__subclasscheck__',
        '__reduce__', '__reduce_ex__',
        '__getstate__', '__setstate__',
        '__copy__', '__deepcopy__'
    )

    _display_cache = {}
    _real_cache = {}

    def __init__(self, display=display_none, real=real_none):
        if display is not display_none:
            base = type(display)
            if base not in self._display_cache:
                self._display_cache[base] = type(
                    f"DisplayWrapper_{base.__name__}",
                    (base,),
                    {}
                )
            self._display = self._display_cache[base](display)
        else:
            self._display = display_none

        if real is not real_none:
            base = type(real)
            if base not in self._real_cache:
                self._real_cache[base] = type(
                    f"RealWrapper_{base.__name__}",
                    (base,),
                    {}
                )
            self._real = self._real_cache[base](real)
        else:
            self._real = real_none

    def __getattr__(self, name):
        if name in ('_display', '_real', '__dict__', '__class__', 'DISPLAY', 'REAL', 'PASSTHROUGH'):
            return super().__getattribute__(name)

        if name in self.DISPLAY:
            target = self._display
            if target is display_none:
                raise AttributeError(f"display object has no attribute '{name}'")
        elif name in self.REAL or name in self.PASSTHROUGH:
            target = self._real
            if target is real_none:
                raise AttributeError(f"real object has no attribute '{name}'")
        else:
            if self._real is not real_none and hasattr(self._real, name):
                target = self._real
            elif self._display is not display_none and hasattr(self._display, name):
                target = self._display
            else:
                raise AttributeError(f"'{type(self).__name__}' has no attribute '{name}'")
        try:
            attr = getattr(target, name)
        except AttributeError:
            raise AttributeError(f"'{type(target).__name__}' has no attribute '{name}'")

        if callable(attr):
            def wrapped(*args, **kwargs):
                result = attr(*args, **kwargs)
                if self._real is not real_none and isinstance(result, type(self._real)):
                    return DisplayProxy(self._display, result)
                return result

            return wrapped

        return attr

    def __repr__(self):
        if self._display is display_none and self._real is real_none:
            return f"<{self.__class__.__name__} empty>"
        return f"DisplayProxy({self._display!r}, {self._real!r})"

def _make_comparison_method(name):

    def method(self, other):
        if self._real is not real_none:
            if isinstance(other, DisplayProxy):
                if other._real is not real_none:
                    other_value = other._real
                else:
                    raise TypeError(f"'{name}' not supported: other has no 'real' value")
            else:
                other_value = other

            return getattr(self._real, name)(other_value)

        raise TypeError(f"'{name}' not supported: this object has no 'real' value")

    method.__name__ = name
    return method

for method_name in ('__lt__', '__le__', '__eq__', '__ne__', '__gt__', '__ge__'):
    setattr(DisplayProxy, method_name, _make_comparison_method(method_name))

def _bool_method(self):
    if self._real is not real_none:
        if hasattr(self._real, '__bool__'):
            return bool(self._real)
        if hasattr(self._real, '__len__'):
            return len(self._real) != 0
        return True

    raise TypeError("'__bool__' not supported: this object has no 'real' value")

setattr(DisplayProxy, '__bool__', _bool_method)