from .._PackageTools import private

class Debug:
    """A debugging wrapper that prints what happens to the wrapped object.

        Use this type to inspect how a value is used at runtime. Debug wraps a
        value and forwards operations to it while printing events such as
        construction, deletion, attribute changes, method calls, arithmetic
        results, and container mutations. It inherits from the type of the
        wrapped value, so it can be used almost anywhere the original value
        could be used.

        This class is meant for debugging, not for production code.slang. The printed
        output and the extra wrapper layer add overhead and side effects.

        Events are printed by _on_change, which can be overridden in a subclass
        to collect or redirect the output instead of printing.

        Example:
            >>> d = Debug([1, 2, 3])
            <<init>> Debug[list][140234...]:[1, 2, 3]
            >>> d.append(4)
            <<container_mutation{...}>> Debug[list][140234...]:[1, 2, 3, 4]
            >>> d + [5]
            <<value_change{...}>> Debug[list][...]:[1, 2, 3, 4, 5]
        """
    _cache = {}

    def __init__(self, value) -> None:
        if getattr(self, '_initialized', False):
            return
        object.__setattr__(self, '_initialized', True)
        if not isinstance(value, (int, float, str, tuple, frozenset, bytes, bool)):
            self.value = value
        print(f"<<init>> {str(self)}")

    def __del__(self) -> None:
        print(f"<<delete>> {str(self)}")

    def __repr__(self):
        name_type = self.__class__.__bases__[1].__name__ if len(self.__class__.__bases__) > 1 else "object"
        value = getattr(self, 'value', getattr(self, '_original', None))
        if value is None:
            name_type = "NoneType"
        elif isinstance(value, bool):
            name_type = "bool"
        return f"Debug[{name_type}][{id(self)}]:{value}"

    def __new__(cls, obj):
        base = type(obj)
        if base not in cls._cache:
            if base in (bool, type(None)):
                bases = (cls,)
            else:
                bases = (cls, base)

            arithmetic_methods = [
                '__add__', '__sub__', '__mul__', '__truediv__', '__floordiv__',
                '__mod__', '__pow__', '__lshift__', '__rshift__', '__and__',
                '__or__', '__xor__', '__radd__', '__rsub__', '__rmul__',
                '__rtruediv__', '__rfloordiv__', '__rmod__', '__rpow__',
                '__rlshift__', '__rrshift__', '__rand__', '__ror__', '__rxor__',
                '__neg__', '__pos__', '__abs__', '__invert__',
                '__iadd__', '__isub__', '__imul__', '__itruediv__', '__ifloordiv__',
                '__imod__', '__ipow__', '__ilshift__', '__irshift__',
                '__iand__', '__ior__', '__ixor__'
            ]

            methods = {name: cls._make_wrapper(name, base) for name in arithmetic_methods}

            if issubclass(base, (list, dict, set, bytearray)):
                mutation_methods = [
                    '__setitem__', '__delitem__',
                    'append', 'extend', 'insert', 'pop', 'remove', 'clear',
                    'update', 'setdefault', 'add', 'discard',
                    'sort', 'reverse'
                ]
                methods.update({name: cls._make_mutation_wrapper(name) for name in mutation_methods})

                protocol_methods = ['__len__', '__getitem__', '__delitem__', '__iter__', '__contains__']
                for name in protocol_methods:
                    if name not in methods:
                        methods[name] = cls._make_protocol_wrapper(name, base)

            cls._cache[base] = type(
                f"Debug[{base.__name__}]",
                bases,
                methods
            )

        new_cls = cls._cache[base]

        if obj is None:
            instance = super().__new__(new_cls)
            instance._original = None
            instance._value = None
            return instance

        if base is bool:
            instance = super().__new__(new_cls)
            instance._original = obj
            instance._value = obj
            return instance

        if issubclass(base, (int, float, str, tuple, frozenset, bytes)):
            instance= base.__new__(new_cls, obj)
            instance._original = obj
            return instance

        instance = base.__new__(new_cls)
        instance._original = obj
        instance._value = obj
        return instance

    @staticmethod
    @private
    def _make_wrapper(method_name, base):
        def wrapper(self, *args, **kwargs):
            old_value = getattr(self, 'value', getattr(self, '_original', None))
            original_obj = getattr(self, '_original', self)
            try:
                method = getattr(original_obj, method_name)
            except AttributeError:
                if method_name.startswith('__i') and method_name.endswith('__'):
                    fallback_name = '__' + method_name[3:]
                    method = getattr(original_obj, fallback_name)
                else:
                    raise
            result = method(*args, **kwargs)
            if old_value is not None and result != old_value:
                self._on_change(
                    'value_change',
                    operation=method_name,
                    old=old_value,
                    new=result,
                    args=args,
                    kwargs=kwargs
                )
                self.value = result
                self._original = result

            if isinstance(result, base) and not isinstance(result, Debug):
                return type(self)(result)
            return result

        return wrapper

    @staticmethod
    @private
    def _make_mutation_wrapper(method_name):
        def wrapper(self, *args, **kwargs):
            before = self._snapshot()
            original_obj = getattr(self, '_original', self)
            method = getattr(original_obj, method_name)
            result = method(*args, **kwargs)
            after = self._snapshot()
            if before != after:
                self._on_change(
                    'container_mutation',
                    method=method_name,
                    before=before,
                    after=after,
                    args=args,
                    kwargs=kwargs
                )
            return result

        return wrapper

    @staticmethod
    @private
    def _make_protocol_wrapper(method_name, base):

        def wrapper(self, *args, **kwargs):
            original_obj = getattr(self, '_original', self)
            method = getattr(original_obj, method_name)
            result = method(*args, **kwargs)
            if isinstance(result, base) and not isinstance(result, Debug):
                return type(self)(result)
            return result

        return wrapper

    @private
    def _snapshot(self):
        obj = getattr(self, '_original', getattr(self, 'value', self))
        if isinstance(obj, (list, tuple)):
            return list(obj)
        elif isinstance(obj, dict):
            return dict(obj)
        elif isinstance(obj, set):
            return set(obj)
        elif isinstance(obj, str):
            return str(obj)
        return None

    @private
    def _on_change(self, change_type, **details):
        print(f'<<{change_type}{details}>> {self}')

    def __setattr__(self, name, value):
        if name.startswith('_') or name in ['_original']:
            super().__setattr__(name, value)
            return
        old_value = getattr(self, name, None)
        has_old = hasattr(self, name)
        super().__setattr__(name, value)
        if has_old:
            self._on_change('attr_modify', attr=name, old=old_value, new=value)
        else:
            self._on_change('attr_add', attr=name, value=value)

    def __delattr__(self, name):
        if name.startswith('_') or name in ['_original']:
            super().__delattr__(name)
            return
        old_value = getattr(self, name, None)
        super().__delattr__(name)
        self._on_change('attr_delete', attr=name, old=old_value)

    def __getattribute__(self, name):
        if name in ('_on_change', '_snapshot', '_original', '_value', '__dict__', '__class__'):
            return super().__getattribute__(name)

        try:
            attr = super().__getattribute__(name)
        except AttributeError:
            original = getattr(self, '_original', None)
            if original is not None and hasattr(original, name):
                attr = getattr(original, name)
            else:
                raise
        if callable(attr) and not name.startswith('_') and name not in ('_on_change', '_snapshot'):
            def monitored_method(*args, **kwargs):
                self._on_change('method_call', method=name, args=args, kwargs=kwargs)
                return attr(*args, **kwargs)

            return monitored_method
        return attr