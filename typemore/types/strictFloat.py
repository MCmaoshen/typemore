from __future__ import annotations
from decimal import Decimal

class StrictFloat(float):
    """A float subclass that does arithmetic with Decimal, free of binary
        floating-point error in a single operation.

        StrictFloat inherits from float, so it can be passed anywhere a float is
        expected. Every arithmetic and comparison operation first converts its
        operands to Decimal, so an expression such as 0.1 + 0.2 produces 0.3
        exactly, without the binary floating-point error that a plain float
        would show.

        Each operation converts its result back to float before wrapping it in a
        new StrictFloat. Accuracy is guaranteed for a single operation, not for a
        chain of operations. For exact arbitrary-precision arithmetic, use
        decimal.Decimal directly.

        Warning:
            Defining __eq__ without defining __hash__ makes instances unhashable,
            so StrictFloat cannot be used as a dictionary key or set member.

        Example:
            >>> 0.1 + 0.2
            0.30000000000000004
            >>> StrictFloat(0.1) + StrictFloat(0.2)
            StrictFloat:0.3
            >>> StrictFloat(0.1) + StrictFloat(0.2) == StrictFloat(0.3)
            True
        """
    def __init__(self, value: StrictFloat | int | float):
        self._dec = Decimal(str(value))

    def __add__(self, other: StrictFloat | int | float):
        if not isinstance(other, StrictFloat | int | float):
            return NotImplemented
        if isinstance(other, StrictFloat):
            return StrictFloat(float(self._dec + other._dec))
        return StrictFloat(float(self._dec + Decimal(str(other))))

    def __radd__(self, other: StrictFloat | int | float):
        return self.__add__(other)

    def __sub__(self, other: StrictFloat | int | float):
        if isinstance(other, StrictFloat):
            return StrictFloat(float(self._dec - other._dec))
        return StrictFloat(float(self._dec - Decimal(str(other))))

    def __rsub__(self, other: StrictFloat | int | float):
        return StrictFloat(float(Decimal(str(other)) - self._dec))

    def __mul__(self, other: StrictFloat | int | float):
        if isinstance(other, StrictFloat):
            return StrictFloat(float(self._dec * other._dec))
        return StrictFloat(float(self._dec * Decimal(str(other))))

    def __rmul__(self, other: StrictFloat | int | float):
        return self.__mul__(other)

    def __truediv__(self, other: StrictFloat | int | float):
        if isinstance(other, StrictFloat):
            return StrictFloat(float(self._dec / other._dec))
        return StrictFloat(float(self._dec / Decimal(str(other))))

    def __rtruediv__(self, other: StrictFloat | int | float):
        return StrictFloat(float(Decimal(str(other)) / self._dec))

    def __floordiv__(self, other: StrictFloat | int | float):
        if isinstance(other, StrictFloat):
            return StrictFloat(float(self._dec // other._dec))
        return StrictFloat(float(self._dec // Decimal(str(other))))

    def __rfloordiv__(self, other: StrictFloat | int | float):
        return StrictFloat(float(Decimal(str(other)) // self._dec))

    def __mod__(self, other: StrictFloat | int | float):
        if isinstance(other, StrictFloat):
            return StrictFloat(float(self._dec % other._dec))
        return StrictFloat(float(self._dec % Decimal(str(other))))

    def __rmod__(self, other: StrictFloat | int | float):
        return StrictFloat(float(Decimal(str(other)) % self._dec))

    def __divmod__(self, other: StrictFloat | int | float):
        if isinstance(other, StrictFloat):
            quotient, remainder = divmod(self._dec, other._dec)
        else:
            quotient, remainder = divmod(self._dec, Decimal(str(other)))
        return float(quotient), float(remainder)

    def __pow__(self, other: StrictFloat | int | float, mod = None):
        if mod is not None:
            raise TypeError("'StrictFloat' does not support 3-argument pow()")
        if isinstance(other, StrictFloat):
            return StrictFloat(float(self._dec ** other._dec))
        return StrictFloat(float(self._dec ** Decimal(str(other))))

    def __rpow__(self, other: StrictFloat | int | float, mod = None):
        if mod is not None:
            raise TypeError("'StrictFloat' does not support 3-argument pow()")
        return StrictFloat(float(Decimal(str(other)) ** self._dec))

    def __neg__(self):
        return StrictFloat(float(-self._dec))

    def __pos__(self):
        return self

    def __hash__(self):
        return hash(self._dec)

    def __abs__(self):
        return StrictFloat(float(abs(self._dec)))

    def __round__(self, n=0):
        return StrictFloat(float(round(self._dec, n)))

    def __trunc__(self):
        return int(self._dec)

    def __floor__(self):
        from math import floor
        return floor(float(self._dec))

    def __ceil__(self):
        from math import ceil
        return ceil(float(self._dec))

    def __float__(self):
        return float(self._dec)

    def __int__(self):
        return int(self._dec)

    def __repr__(self):
        return f"StrictFloat:{float(self._dec)}"

    def __str__(self):
        return str(float(self._dec))

    def __eq__(self, other):
        if isinstance(other, StrictFloat):
            return self._dec == other._dec
        return self._dec == Decimal(str(other))

    def __ne__(self, other):
        return not self.__eq__(other)

    def __lt__(self, other: StrictFloat | int | float):
        if isinstance(other, StrictFloat):
            return self._dec < other._dec
        return self._dec < Decimal(str(other))

    def __le__(self, other: StrictFloat | int | float):
        if isinstance(other, StrictFloat):
            return self._dec <= other._dec
        return self._dec <= Decimal(str(other))

    def __gt__(self, other: StrictFloat | int | float):
        if isinstance(other, StrictFloat):
            return self._dec > other._dec
        return self._dec > Decimal(str(other))

    def __ge__(self, other: StrictFloat | int | float):
        if isinstance(other, StrictFloat):
            return self._dec >= other._dec
        return self._dec >= Decimal(str(other))

a = StrictFloat(1.2)
print({a: 1})