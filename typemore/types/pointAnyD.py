from __future__ import annotations

class PointAnyD:
    """A point with any number of dimensions, stored as numbered attributes.

        PointAnyD takes any number of numbers and stores them as attributes
        "0", "1", "2", and so on. All operations work on every component, and
        two points must have the same number of dimensions to be combined.

        Comparison is partial: p < q is True only if every component of p is
        less than the corresponding component of q. Points with different
        dimensions cannot be compared.

        Example:
            >>> p = PointAnyD(1, 2, 3)
            >>> p[0]
            1
            >>> p + 1
            PointAnyD[3D](2, 3, 4)
            >>> p + PointAnyD(10, 20, 30)
            PointAnyD[3D](11, 22, 33)
        """
    def __init__(self, *args: int | float):
        for i in range(len(args)):
            setattr(self, str(i), args[i])
        #__slots__ = (i for i in range(len(vars(self))))

    def __repr__(self):
        return_str = "PointAnyD" + f"[{len(vars(self))}D]" + "("
        for i in range(len(vars(self))):
            _ = vars(self)[str(i)]
            return_str += f"{_}, "
        if len(return_str) < 15:
            pass
        else:
            return_str = return_str[:-2]
        return return_str + ")"

    def __str__(self):
        return_str = '('
        for i in range(len(vars(self))):
            _ = vars(self)[str(i)]
            return_str += f"{_}, "
        if len(return_str) < 4:
            pass
        else:
            return_str = return_str[:-2]
        return return_str + ")"

    def __eq__(self, other):
        if not isinstance(other, PointAnyD) or len(vars(self)) != len(vars(other)):
            return False
        for s, o in zip(self.__dict__.values(), other.__dict__.values()):
            if s != o:
                return False
        return True

    def __ne__(self, other):
        return not self.__eq__(other)

    def __lt__(self, other: PointAnyD):
        if not isinstance(other, PointAnyD):
            return NotImplemented
        if len(vars(self)) != len(vars(other)):
            raise NotImplementedError(f"different number of elements: {len(vars(self))} and {len(vars(other))}")
        for s, o in zip(self.__dict__.values(), other.__dict__.values()):
            if s >= o:
                return False
        return True

    def __le__(self, other: PointAnyD):
        if not isinstance(other, PointAnyD):
            return NotImplemented
        if len(vars(self)) != len(vars(other)):
            raise NotImplementedError(f"different number of elements: {len(vars(self))} and {len(vars(other))}")
        for s, o in zip(self.__dict__.values(), other.__dict__.values()):
            if s > o:
                return False
        return True

    def __gt__(self, other: PointAnyD):
        if not isinstance(other, PointAnyD):
            return NotImplemented
        if len(vars(self)) != len(vars(other)):
            raise NotImplementedError(f"different number of elements: {len(vars(self))} and {len(vars(other))}")
        for s, o in zip(self.__dict__.values(), other.__dict__.values()):
            if s <= o:
                return False
        return True

    def __ge__(self, other: PointAnyD):
        if not isinstance(other, PointAnyD):
            return NotImplemented
        if len(vars(self)) != len(vars(other)):
            raise NotImplementedError(f"different number of elements: {len(vars(self))} and {len(vars(other))}")
        for s, o in zip(self.__dict__.values(), other.__dict__.values()):
            if s < o:
                return False
        return True

    def __getitem__(self, index: int):
        if not isinstance(index, int):
            raise TypeError("Index must be an integer")
        max_index = len(vars(self)) - 1
        if index > max_index:
            raise IndexError("Index out of range")
        return self.__dict__[str(index)]

    def __setitem__(self, index: int, value: int | float):
        if not isinstance(index, int):
            raise TypeError("Index must be an integer")
        max_index = len(vars(self)) - 1
        if index > max_index:
            raise IndexError("Index out of range")
        self.__dict__[str(index)] = value

    def __len__(self):
        return len(vars(self))

    def __iter__(self):
        current = 0
        while current <= len(self.__dict__.values()) - 1:
            yield self.__dict__[str(current)]
            current += 1

    def __contains__(self, item: int | float):
        if not isinstance(item, int | float):
            raise TypeError(f"argument must be 'int' or 'float', not '{type(item).__name__}'")
        return item in self.__dict__.values()

    def __add__(self, other: PointAnyD | int | float):
        if not isinstance(other, PointAnyD | int | float):
            return NotImplemented
        if len(vars(self)) != len(vars(other)):
            raise NotImplementedError(f"different number of elements: {len(vars(self))} and {len(vars(other))}")
        if isinstance(other, int | float):
            return PointAnyD(*(i + other for i in self.__dict__.values()))
        return PointAnyD(*(i + j for i, j in zip(self.__dict__.values(), other.__dict__.values())))

    def __sub__(self, other: PointAnyD | int | float):
        if not isinstance(other, PointAnyD | int | float):
            return NotImplemented
        if len(vars(self)) != len(vars(other)):
            raise NotImplementedError(f"different number of elements: {len(vars(self))} and {len(vars(other))}")
        if isinstance(other, int | float):
            return PointAnyD(*(i - other for i in self.__dict__.values()))
        return PointAnyD(*(i - j for i, j in zip(self.__dict__.values(), other.__dict__.values())))

    def __mul__(self, other: PointAnyD | int | float):
        if not isinstance(other, PointAnyD | int | float):
            return NotImplemented
        if len(vars(self)) != len(vars(other)):
            raise NotImplementedError(f"different number of elements: {len(vars(self))} and {len(vars(other))}")
        if isinstance(other, int | float):
            return PointAnyD(*(i * other for i in self.__dict__.values()))
        return PointAnyD(*(i * j for i, j in zip(self.__dict__.values(), other.__dict__.values())))

    def __truediv__(self, other: PointAnyD | int | float):
        if not isinstance(other, PointAnyD | int | float):
            return NotImplemented
        if len(vars(self)) != len(vars(other)):
            raise NotImplementedError(f"different number of elements: {len(vars(self))} and {len(vars(other))}")
        if isinstance(other, int | float):
            return PointAnyD(*(i / other for i in self.__dict__.values()))
        return PointAnyD(*(i / j for i, j in zip(self.__dict__.values(), other.__dict__.values())))

    def __floordiv__(self, other: PointAnyD | int | float):
        if not isinstance(other, PointAnyD | int | float):
            return NotImplemented
        if len(vars(self)) != len(vars(other)):
            raise NotImplementedError(f"different number of elements: {len(vars(self))} and {len(vars(other))}")
        if isinstance(other, int | float):
            return PointAnyD(*(i // other for i in self.__dict__.values()))
        return PointAnyD(*(i // j for i, j in zip(self.__dict__.values(), other.__dict__.values())))

    def __mod__(self, other: PointAnyD | int | float):
        if not isinstance(other, PointAnyD | int | float):
            return NotImplemented
        if len(vars(self)) != len(vars(other)):
            raise NotImplementedError(f"different number of elements: {len(vars(self))} and {len(vars(other))}")
        if isinstance(other, int | float):
            return PointAnyD(*(i % other for i in self.__dict__.values()))
        return PointAnyD(*(i % j for i, j in zip(self.__dict__.values(), other.__dict__.values())))

    def __pow__(self, other: PointAnyD | int | float):
        if not isinstance(other, PointAnyD | int | float):
            return NotImplemented
        if len(vars(self)) != len(vars(other)):
            raise NotImplementedError(f"different number of elements: {len(vars(self))} and {len(vars(other))}")
        if isinstance(other, int | float):
            return PointAnyD(*(i ** other for i in self.__dict__.values()))
        return PointAnyD(*(i ** j for i, j in zip(self.__dict__.values(), other.__dict__.values())))

    def __pos__(self):
        return self

    def __neg__(self):
        return PointAnyD(*(-i for i in self.__dict__.values()))

    def __delattr__(self, item):
        raise NotImplementedError(f"Cannot delete attribute {item}")