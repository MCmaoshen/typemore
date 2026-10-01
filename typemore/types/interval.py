from __future__ import annotations
from typemore._PackageTools import private

class Interval:
    """A numeric interval with independent open or closed endpoints.

        Each endpoint carries a boolean: True means closed (inclusive), False
        means open (exclusive). So Interval(True, 1, 5, False) represents [1, 5),
        which contains 1 but not 5. A single-point interval must be closed on
        both ends.

        Comparison by the interval_* and __lt__ family uses length first, then
        the endpoint states as a tiebreaker. interval_add and interval_sub
        treat an Interval and a number differently; see each method for details.

        Example:
            >>> 3 in Interval(True, 1, 5, False)
            True
            >>> 5 in Interval(True, 1, 5, False)
            False
            >>> Interval(True, 1, 5, False) + 2
            Interval(True, 3, 7, False)
            >>> Interval(True, 1, 5, False).interval_add(Interval(True, 0, 4, True))
            Interval(True, 0, 5, True)
        """
    __slots__ = ("left", "start", "end", "right")

    def __init__(self, left: bool,  start: int | float, end: int | float, right: bool):
        super().__setattr__("left", left)
        super().__setattr__("start", start)
        super().__setattr__("end", end)
        super().__setattr__("right", right)
        if self.start > self.end:
            raise ValueError(f"start {self.start} is greater than end {self.end}")
        if self.start == self.end and(not self.left and not self.right):
            raise ValueError(f"single point interval must be a closed interval")

    def __repr__(self):
        return f"Interval({self.left}, {self.start}, {self.end}, {self.right})"

    def __str__(self):
        str_left = '[' if self.left else '('
        str_right = ']' if self.right else ')'
        return f"{str_left}{self.start}, {self.end}{str_right}"

    def __setattr__(self, name, value: int | float | bool):
        if name == "start":
            if hasattr(self, 'end') and value > self.end:
                raise ValueError(f"start {self.start} is greater than end {self.end}")
        elif name == "end":
            if hasattr(self, 'start') and value < self.start:
                raise ValueError(f"start {self.start} is less than end {self.end}")
        elif name in ("left", "right"):
            if not isinstance(value, bool):
                raise TypeError(f"{name} must be bool")
        super().__setattr__(name, value)

    def __delattr__(self, item):
        raise NotImplementedError(f"Cannot delete attribute {item}")

    @private
    def _state(self, other):
        """Record the open or closed state of both intervals for error messages.

            Sets left_state and right_state on self and on other to either 'close'
            or 'open', based on the corresponding booleans.

            This is a private helper. Do not call it from outside the class.
            """
        return (
            'close' if self.left else 'open',
            'close' if self.right else 'open',
            'close' if other.left else 'open',
            'close' if other.right else 'open'
        )

    def interval_eq(self, other: Interval) -> bool:
        """Return True if both intervals have the same length and the same
            endpoint states.

            Endpoint states are compared by how many ends are closed. So [1, 5) and
            (1, 5] are equal by this method.
            """
        if not isinstance(other, Interval):
            return False
        return self.end - self.start == other.end - other.start and self.left + self.right == other.left + other.right

    def interval_lt(self, other: Interval) -> bool:
        """Return True if this interval is shorter than other.

            When lengths are equal, compare by endpoint states.

            Raises TypeError if other is not an Interval.
            """
        if not isinstance(other, Interval):
            raise TypeError(f"'<' not supported between instances of '{type(self).__name__}' and '{type(other).__name__}'")
        return (self.end - self.start < other.end - other.start) if (
                self.end - self.start != other.end - other.start) else (
                self.left + self.right < other.left + other.right)

    def interval_le(self, other: Interval) -> bool:
        """Return True if this interval is shorter than or equal to other.

            When lengths are equal, compare by endpoint states.

            Raises TypeError if other is not an Interval.
            """
        if not isinstance(other, Interval):
            raise TypeError(f"'<=' not supported between instances of '{type(self).__name__}' and '{type(other).__name__}'")
        return (self.end - self.start <= other.end - other.start) if (
                self.end - self.start != other.end - other.start) else (
                self.left + self.right <= other.left + other.right)

    def interval_ne(self, other: Interval) -> bool:
        """Return True if the two intervals differ in length or in endpoint states.

            This is the negation of interval_eq.
            """
        return not self.interval_eq(other)

    def interval_gt(self, other: Interval) -> bool:
        """Return True if this interval is longer than other.

            When lengths are equal, compare by endpoint states.

            Raises TypeError if other is not an Interval.
            """
        if not isinstance(other, Interval):
            raise TypeError(f"'>' not supported between instances of '{type(self).__name__}' and '{type(other).__name__}'")
        return (self.end - self.start > other.end - other.start) if (
                    self.end - self.start != other.end - other.start) else (
                    self.left + self.right > other.left + other.right)

    def interval_ge(self, other: Interval) -> bool:
        """Return True if this interval is longer than or equal to other.

            When lengths are equal, compare by endpoint states.

            Raises TypeError if other is not an Interval.
            """
        if not isinstance(other, Interval):
            raise TypeError(f"'>=' not supported between instances of '{type(self).__name__}' and '{type(other).__name__}'")
        return (self.end - self.start >= other.end - other.start) if (
                    self.end - self.start != other.end - other.start) else (
                    self.left + self.right >= other.left + other.right)

    def interval_add(self, other: Interval | int | float):
        """Combine this interval with another interval or a number.

            With a number, expand both ends outward by that amount, keeping the same
            endpoint states.

            With another Interval, return the smallest Interval covering both. The
            endpoint that reaches farther outward wins; when both reach equally far,
            the closed end wins over the open one.
            """
        if not isinstance(other, Interval | int | float):
            raise TypeError(f"unsupported operand type(s) for +: '{type(self).__name__}' and '{type(other).__name__}'")
        if isinstance(other, int | float):
            return Interval(self.left, self.start - other, self.end + other, self.right)
        if self.start < other.start:
            add_start = self.start
            add_left = self.left
        elif self.start > other.start:
            add_start = other.start
            add_left = other.left
        else:
            add_start = self.start
            add_left = other.left if other.left > self.left else self.left
        if self.end > other.end:
            add_end = self.end
            add_right = self.right
        elif self.end < other.end:
            add_end = other.end
            add_right = other.right
        else:
            add_end = self.end
            add_right = other.right if other.right > self.right else self.right
        return Interval(add_left, add_start, add_end, add_right)

    def interval_sub(self, other: Interval | int | float):
        """Subtract another interval or a number from this interval.

            With a number, shrink both ends inward by that amount, keeping the same
            endpoint states.

            With another Interval, return the parts of this interval not covered by
            other. The result depends on how the two overlap:

            - other is fully inside this interval: return a tuple of two Intervals,
              with the inner endpoints flipped.
            - other overlaps the right side: return the uncovered left part.
            - other overlaps the left side: return the uncovered right part.
            - any other case: return None.
            """
        if not isinstance(other, Interval | int | float):
            raise TypeError(f"unsupported operand type(s) for -: '{type(self).__name__}' and '{type(other).__name__}'")
        if isinstance(other, int | float):
            end_start = self.start + other
            end_end = self.end - other
            if end_start > end_end:
                raise ValueError(f"start {end_start} is greater than end {end_end}")
            return Interval(self.left, end_start, end_end, self.right)
        if self.start < other.start and self.end > other.end:
            return Interval(self.left, self.start, other.start, not other.left), Interval(not other.right, other.end, self.end, self.right)
        elif self.start < other.start and self.end < other.end:
            return Interval(self.left, self.start, other.start, not other.left)
        elif self.start > other.start and self.end > other.end:
            return Interval(not other.left, other.start, self.end, self.right)
        return None

    def __contains__(self, number: int | float) -> bool:
        if not isinstance(number, int | float):
            raise TypeError(f"argument must be 'int' or 'float', not '{type(number).__name__}'")
        if self.left == True and self.right == True:return self.start <= number <= self.end
        elif self.left == True and self.right == False:return self.start <= number < self.end
        elif self.left == False and self.right == True:return self.start < number <= self.end
        else:return self.start < number < self.end

    def __eq__(self, other) -> bool:
        if not isinstance(other, Interval):
            return False
        return self.start == other.start and self.end == other.end and self.left + self.right == other.left + other.right

    def __ne__(self, other) -> bool:
        return not self.__eq__(other)

    def __lt__(self, other: Interval | int | float) -> bool:
        if not isinstance(other, Interval | int | float):
            return NotImplemented
        if isinstance(other, int | float):
            return self.start < other and self.end < other
        return self.start < other.start and self.end < other.end

    def __le__(self, other: Interval | int | float) -> bool:
        if not isinstance(other, Interval | int | float):
            return NotImplemented
        if isinstance(other, int | float):
            return self.start <= other and self.end <= other
        return self.start <= other.start and self.end <= other.end

    def __gt__(self, other: Interval | int | float) -> bool:
        if not isinstance(other, Interval | int | float):
            return NotImplemented
        if isinstance(other, int | float):
            return self.start > other and self.end > other
        return self.start > other.start and self.end > other.end

    def __ge__(self, other: Interval | int | float) -> bool:
        if not isinstance(other, Interval | int | float):
            return NotImplemented
        if isinstance(other, int | float):
            return self.start >= other and self.end >= other
        return self.start >= other.start and self.end >= other.end

    def __add__(self, other: Interval | int | float):
        if not isinstance(other, Interval | int | float):
            return NotImplemented
        if isinstance(other, int | float):
            return Interval(self.left, self.start + other, self.end + other, self.right)
        if self.left == other.left and self.right == other.right:
            return Interval(self.left, self.start + other.start, self.end + other.end, self.right)
        else:
            self_left, self_right, other_left, other_right = self._state(other)
            raise ValueError(f"different interval types: {self_left}, {self_right} + {other_left}, {other_right}")

    def __sub__(self, other: Interval | int | float):
        if not isinstance(other, Interval | int | float):
            return NotImplemented
        if isinstance(other, int | float):
            return Interval(self.left, self.start - other, self.end - other, self.right)
        if self.left == other.left and self.right == other.right:
            return Interval(self.left, self.start - other.start, self.end - other.end, self.right)
        else:
            self_left, self_right, other_left, other_right = self._state(other)
            raise ValueError(f"different interval types: {self_left}, {self_right} - {other_left}, {other_right}")

    def __mul__(self, other: Interval | int | float):
        if not isinstance(other, Interval | int | float):
            return NotImplemented
        if isinstance(other, int | float):
            return Interval(self.left, self.start * other, self.end * other, self.right)
        if self.left == other.left and self.right == other.right:
            return Interval(self.left, self.start * other.start, self.end * other.end, self.right)
        else:
            self_left, self_right, other_left, other_right = self._state(other)
            raise ValueError(f"different interval types: {self_left}, {self_right} * {other_left}, {other_right}")

    def __truediv__(self, other: Interval | int | float):
        if not isinstance(other, Interval | int | float):
            return NotImplemented
        if isinstance(other, int | float):
            return Interval(self.left, self.start / other, self.end / other, self.right)
        if self.left == other.left and self.right == other.right:
            return Interval(self.left, self.start / other.start, self.end / other.end, self.right)
        else:
            self_left, self_right, other_left, other_right = self._state(other)
            raise ValueError(f"different interval types: {self_left}, {self_right} / {other_left}, {other_right}")

    def __floordiv__(self, other: Interval | int | float):
        if not isinstance(other, Interval | int | float):
            return NotImplemented
        if isinstance(other, int | float):
            return Interval(self.left, self.start // other, self.end // other, self.right)
        if self.left == other.left and self.right == other.right:
            return Interval(self.left, self.start // other.start, self.end // other.end, self.right)
        else:
            self_left, self_right, other_left, other_right = self._state(other)
            raise ValueError(f"different interval types: {self_left}, {self_right} // {other_left}, {other_right}")

    def __mod__(self, other: Interval | int | float):
        if not isinstance(other, Interval | int | float):
            return NotImplemented
        if isinstance(other, int | float):
            return Interval(self.left, self.start % other, self.end % other, self.right)
        if self.left == other.left and self.right == other.right:
            return Interval(self.left, self.start % other.start, self.end % other.end, self.right)
        else:
            self_left, self_right, other_left, other_right = self._state(other)
            raise ValueError(f"different interval types: {self_left}, {self_right} % {other_left}, {other_right}")

    def __pow__(self, other: Interval | int | float):
        if not isinstance(other, Interval | int | float):
            return NotImplemented
        if isinstance(other, int | float):
            return Interval(self.left, self.start ** other, self.end ** other, self.right)
        if self.left == other.left and self.right == other.right:
            return Interval(self.left, self.start ** other.start, self.end ** other.end, self.right)
        else:
            self_left, self_right, other_left, other_right = self._state(other)
            raise ValueError(f"different interval types: {self_left}, {self_right} ** {other_left}, {other_right}")

    def __pos__(self) -> 'Interval':
        return self

    def __neg__(self) -> 'Interval':
        return Interval(self.right, -self.end, -self.start, self.left)


a = Interval(True, 1, 20, True)
b = Interval(True, -10, 200, False)

print(a+b)