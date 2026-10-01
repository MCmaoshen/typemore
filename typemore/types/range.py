from __future__ import annotations

class Range:
    """A closed interval [start, end] of numbers.

        Both bounds are inclusive. start must not be greater than end. A Range
        supports comparison, containment, and element-wise arithmetic with
        another Range or a single number.

        Example:
            >>> r = Range(1, 5)
            >>> 3 in r
            True
            >>> Range(1, 3) + 2
            Range(3, 5)
            >>> Range(0, 2).range_add(Range(1, 3))
            Range(0, 3)
        """
    __slots__ = ("start", "end")

    def __init__(self, start: int | float, end: int | float):
        self.start = start
        self.end = end
        if self.start > self.end:
            raise ValueError(f"start {self.start} is greater than end {self.end}")

    def __repr__(self):
        return f"Range({self.start}, {self.end})"

    def __str__(self):
        return f"({self.start}, {self.end})"

    def range_eq(self, other: Range):
        """Return True if both ranges have the same length.

            Length means end - start, not the pair of bounds. So Range(0, 5) and
            Range(10, 15) are equal by this method.
            """
        if not isinstance(other, Range):
            return False
        return self.end - self.start == other.end - other.start
    
    def range_lt(self, other: Range):
        """Return True if this range is shorter than other.

            Raises TypeError if other is not a Range.
            """
        if not isinstance(other, Range):
            raise TypeError(f"'<' not supported between instances of '{type(self).__name__}' and '{type(other).__name__}'")
        return self.end - self.start < other.end - other.start

    def range_le(self, other: Range):
        """Return True if this range is shorter than or equal to other.

            Raises TypeError if other is not a Range.
            """
        if not isinstance(other, Range):
            raise TypeError(f"'<=' not supported between instances of '{type(self).__name__}' and '{type(other).__name__}'")
        return self.end - self.start <= other.end - other.start

    def range_ne(self, other: Range):
        """Return True if the two ranges have different lengths.

            This is the negation of range_eq.
            """
        return not self.range_eq(other)

    def range_gt(self, other: Range):
        """Return True if this range is longer than other.

            Raises TypeError if other is not a Range.
            """
        if not isinstance(other, Range):
            raise TypeError(f"'>' not supported between instances of '{type(self).__name__}' and '{type(other).__name__}'")
        return self.end - self.start > other.end - other.start

    def range_ge(self, other: Range):
        """Return True if this range is longer than or equal to other.

            Raises TypeError if other is not a Range.
            """
        if not isinstance(other, Range):
            raise TypeError(f"'>=' not supported between instances of '{type(self).__name__}' and '{type(other).__name__}'")
        return self.end - self.start >= other.end - other.start

    def range_add(self, other: Range | int | float):
        """Combine this range with another range or a number.

            With a number, expand the range outward on both ends by that
            amount. With another Range, return the smallest Range covering both.
            """
        if not isinstance(other, Range | int | float):
            raise TypeError(f"unsupported operand type(s) for +: '{type(self).__name__}' and '{type(other).__name__}'")
        if isinstance(other, int | float):
            return Range(self.start - other, self.end + other)
        if self.start < other.start:
            add_start = self.start
        else:
            add_start = other.start
        if self.end < other.end:
            add_end = other.end
        else:
            add_end = self.end
        return Range(add_start, add_end)

    def range_sub(self, other: Range | int | float):
        """Subtract another range or a number from this range.

        With a number, the range shrinks inward by that amount. With another
        Range, the result depends on how the two ranges overlap:

        - other covers this range entirely, or extends beyond it on both sides:
          return None.
        - other is fully inside this range: return a tuple of two Ranges, the
          parts before and after other.
        - other overlaps the right side: return the uncovered left part,
          Range(self.start, other.start).
        - other overlaps the left side: return the uncovered right part,
          Range(other.start, self.end).
        - any other case: return None.
        """
        if not isinstance(other, Range | int | float):
            raise TypeError(f"unsupported operand type(s) for -: '{type(self).__name__}' and '{type(other).__name__}'")
        if isinstance(other, int | float):
            end_start = self.start + other
            end_end = self.end - other
            if end_start > end_end:
                raise ValueError(f"start {end_start} is greater than end {end_end}")
            return Range(end_start, end_end)

        if other.start <= self.start and other.end >= self.end:
            return None

        if self.start < other.start and self.end > other.end:
            return Range(self.start, other.start), Range(other.end, self.end)
        elif self.start <= other.start and self.end <= other.end:
            return Range(self.start, other.start)
        elif self.start >= other.start and self.end >= other.end:
            return Range(other.start, self.end)
        return None

    def __contains__(self, number: int | float):
        if not isinstance(number, int | float):
            raise TypeError(f"argument must be 'int' or 'float', not '{type(number).__name__}'")
        return self.start <= number <= self.end

    def __setattr__(self, name, value):
        if name == "start":
            if hasattr(self, 'end') and value > self.end:
                raise ValueError(f"start {self.start} is greater than end {self.end}")
            pass
        elif name == "end":
            if hasattr(self, 'start') and value < self.start:
                raise ValueError(f"start {self.start} is less than end {self.end}")
            pass
        super().__setattr__(name, value)

    def __delattr__(self, item):
        raise NotImplementedError(f"Cannot delete attribute {item}")

    def __eq__(self, other) -> bool:
        if not isinstance(other, Range):
            return False
        return self.start == other.start and self.end == other.end

    def __ne__(self, other) -> bool:
        return not self.__eq__(other)

    def __lt__(self, other: Range | int | float) -> bool:
        if not isinstance(other, Range | int | float):
            return NotImplemented
        if isinstance(other, int | float):
            return self.start < other and self.end < other
        return self.start < other.start and self.end < other.end

    def __le__(self, other: Range | int | float) -> bool:
        if not isinstance(other, Range | int | float):
            return NotImplemented
        if isinstance(other, int | float):
            return self.start <= other and self.end <= other
        return self.start <= other.start and self.end <= other.end

    def __gt__(self, other: Range | int | float) -> bool:
        if not isinstance(other, Range | int | float):
            return NotImplemented
        if isinstance(other, int | float):
            return self.start > other and self.end > other
        return self.start > other.start and self.end > other.end

    def __ge__(self, other: Range | int | float) -> bool:
        if not isinstance(other, Range | int | float):
            return NotImplemented
        if isinstance(other, int | float):
            return self.start >= other and self.end >= other
        return self.start >= other.start and self.end >= other.end

    def __add__(self, other: Range | int | float):
        if not isinstance(other, Range | int | float):
            return NotImplemented
        if isinstance(other, int | float):
            return Range(self.start + other, self.end + other)
        return Range(self.start + other.start, self.end + other.end)

    def __sub__(self, other: Range | int | float):
        if not isinstance(other, Range | int | float):
            return NotImplemented
        if isinstance(other, int | float):
            return Range(self.start - other, self.end - other)
        return Range(self.start - other.start, self.end - other.end)

    def __mul__(self, other: Range | int | float):
        if not isinstance(other, Range | int | float):
            return NotImplemented
        if isinstance(other, int | float):
            return Range(self.start * other, self.end * other)
        return Range(self.start * other.start, self.end * other.end)

    def __truediv__(self, other: Range | int | float):
        if not isinstance(other, Range | int | float):
            return NotImplemented
        if isinstance(other, int | float):
            return Range(self.start / other, self.end / other)
        return Range(self.start / other.start, self.end / other.end)

    def __floordiv__(self, other: Range | int | float):
        if not isinstance(other, Range | int | float):
            return NotImplemented
        if isinstance(other, int | float):
            return Range(self.start // other, self.end // other)
        return Range(self.start // other.start, self.end // other.end)

    def __mod__(self, other: Range | int | float):
        if not isinstance(other, Range | int | float):
            return NotImplemented
        if isinstance(other, int | float):
            return Range(self.start % other, self.end % other)
        return Range(self.start % other.start, self.end % other.end)

    def __pow__(self, other: Range | int | float):
        if not isinstance(other, Range | int | float):
            return NotImplemented
        if isinstance(other, int | float):
            return Range(self.start ** other, self.end ** other)
        return Range(self.start ** other.start, self.end ** other.end)

    def __pos__(self):
        return self

    def __neg__(self):
        return Range(-self.end, -self.start)