from __future__ import annotations

class Point2D:
    """A two-dimensional point with element-wise operations.

        Point2D stores two numbers, x and y. Arithmetic with another Point2D is
        done element by element: (1, 2) + (3, 4) gives (4, 6). Arithmetic with a
        number applies that number to both components: (1, 2) * 3 gives (3, 6).

        Comparison is partial: p < q is True only if both components of p are
        less than the corresponding components of q. Points that are not
        comparable in this way make < return False, not an error. This differs
        from the usual total order of numbers.

        len(p) is always 2, and "in" checks whether a number equals x or y.

        Example:
            >>> Point2D(1, 2) + Point2D(3, 4)
            Point(4, 6)
            >>> Point2D(1, 2) * 3
            Point(3, 6)
            >>> 2 in Point2D(1, 2)
            True
            >>> Point2D(1, 5) < Point2D(2, 3)
            False
        """
    __slots__ = ("x", "y")

    def __init__(self, x: int | float, y: int | float):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"Point({self.x}, {self.y})"

    def __str__(self):
        return f"({self.x}, {self.y})"

    def __eq__(self, other):
        if not isinstance(other, Point2D):
            return False
        return self.x == other.x and self.y == other.y

    def __ne__(self, other):
        return not self.__eq__(other)

    def __lt__(self, other: Point2D):
        if not isinstance(other, Point2D):
            return NotImplemented
        return self.x < other.x and self.y < other.y

    def __le__(self, other: Point2D):
        if not isinstance(other, Point2D):
            return NotImplemented
        return self.x <= other.x and self.y <= other.y

    def __gt__(self, other: Point2D):
        if not isinstance(other, Point2D):
            return NotImplemented
        return self.x > other.x and self.y > other.y

    def __ge__(self, other: Point2D):
        if not isinstance(other, Point2D):
            return NotImplemented
        return self.x >= other.x and self.y >= other.y

    def __len__(self):
        return 2

    def __contains__(self, item: int | float):
        if not isinstance(item, int | float):
            raise TypeError(f"argument must be 'int' or 'float', not '{type(item).__name__}'")
        return item == self.x or item == self.y

    def __add__(self, other: Point2D | int | float):
        if not isinstance(other, Point2D | int | float):
            return NotImplemented
        if isinstance(other, int | float):
            return Point2D(self.x + other, self.y + other)
        return Point2D(self.x + other.x, self.y + other.y)

    def __sub__(self, other: Point2D | int | float):
        if not isinstance(other, Point2D | int | float):
            return NotImplemented
        if isinstance(other, int | float):
            return Point2D(self.x - other, self.y - other)
        return Point2D(self.x - other.x, self.y - other.y)

    def __mul__(self, other: Point2D | int | float):
        if not isinstance(other, Point2D | int | float):
            return NotImplemented
        if isinstance(other, int | float):
            return Point2D(self.x * other, self.y * other)
        return Point2D(self.x * other.x, self.y *other.y)

    def __truediv__(self, other: Point2D | int | float):
        if not isinstance(other, Point2D | int | float):
            return NotImplemented
        if isinstance(other, int | float):
            return Point2D(self.x / other, self.y / other)
        return Point2D(self.x / other.x, self.y / other.y)

    def __floordiv__(self, other: Point2D | int | float):
        if not isinstance(other, Point2D | int | float):
            return NotImplemented
        if isinstance(other, int | float):
            return Point2D(self.x // other, self.y // other)
        return Point2D(self.x // other.x, self.y // other.y)

    def __mod__(self, other: Point2D | int | float):
        if not isinstance(other, Point2D | int | float):
            return NotImplemented
        if isinstance(other, int | float):
            return Point2D(self.x % other, self.y % other)
        return Point2D(self.x % other.x, self.y % other.y)

    def __pow__(self, other: Point2D | int | float):
        if not isinstance(other, Point2D | int | float):
            return NotImplemented
        if isinstance(other, int | float):
            return Point2D(self.x ** other, self.y ** other)
        return Point2D(self.x ** other.x, self.y ** other.y)

    def __pos__(self):
        return self

    def __neg__(self):
        return Point2D(-self.x, -self.y)

    def __delattr__(self, item):
        raise NotImplementedError(f"Cannot delete attribute {item}")