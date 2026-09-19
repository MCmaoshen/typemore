from __future__ import annotations

class Point3D:
    """A three-dimensional point with element-wise operations.

        Point3D stores three numbers, x, y, and z. Arithmetic with another
        Point3D is done element by element: (1, 2, 3) + (4, 5, 6) gives
        (5, 7, 9). Arithmetic with a number applies that number to all three
        components: (1, 2, 3) * 2 gives (2, 4, 6).

        Comparison is partial: p < q is True only if all three components of p
        are less than the corresponding components of q. Points that are not
        comparable in this way make < return False, not an error. This differs
        from the usual total order of numbers.

        len(p) is always 3, and "in" checks whether a number equals x, y, or z.

        Example:
            >>> Point3D(1, 2, 3) + Point3D(4, 5, 6)
            Point(5, 7, 9)
            >>> Point3D(1, 2, 3) * 2
            Point(2, 4, 6)
            >>> 2 in Point3D(1, 2, 3)
            True
            >>> Point3D(1, 5, 2) < Point3D(2, 3, 4)
            False
        """
    __slots__ = ("x", "y", "z")

    def __init__(self, x: int | float, y: int | float, z: int | float):
        self.x = x
        self.y = y
        self.z = z

    def __repr__(self):
        return f"Point({self.x}, {self.y}, {self.z})"

    def __str__(self):
        return f"({self.x}, {self.y}, {self.z})"

    def __eq__(self, other):
        if not isinstance(other, Point3D):
            return False
        return self.x == other.x and self.y == other.y and self.z == other.z

    def __ne__(self, other):
        return not self.__eq__(other)

    def __lt__(self, other: Point3D):
        if not isinstance(other, Point3D):
            return NotImplemented
        return self.x < other.x and self.y < other.y and self.z < other.z

    def __le__(self, other: Point3D):
        if not isinstance(other, Point3D):
            return NotImplemented
        return self.x <= other.x and self.y <= other.y and self.z <= other.z

    def __gt__(self, other: Point3D):
        if not isinstance(other, Point3D):
            return NotImplemented
        return self.x > other.x and self.y > other.y and self.z > other.z

    def __ge__(self, other: Point3D):
        if not isinstance(other, Point3D):
            return NotImplemented
        return self.x >= other.x and self.y >= other.y and self.z >= other.z

    def __len__(self):
        return 3

    def __contains__(self, item: int | float) -> bool:
        if not isinstance(item, int | float):
            raise TypeError(f"argument must be 'int' or 'float', not '{type(item).__name__}'")
        return item == self.x or item == self.y or item == self.z

    def __add__(self, other: Point3D | int | float):
        if not isinstance(other, Point3D | int | float):
            return NotImplemented
        if isinstance(other, int | float):
            return Point3D(self.x + other, self.y + other, self.z + other)
        return Point3D(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other: Point3D | int | float):
        if not isinstance(other, Point3D | int | float):
            return NotImplemented
        if isinstance(other, int | float):
            return Point3D(self.x - other, self.y - other, self.z - other)
        return Point3D(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, other: Point3D | int | float):
        if not isinstance(other, Point3D | int | float):
            return NotImplemented
        if isinstance(other, int | float):
            return Point3D(self.x * other, self.y * other, self.z * other)
        return Point3D(self.x * other.x, self.y * other.y, self.z * other.z)

    def __truediv__(self, other: Point3D | int | float):
        if not isinstance(other, Point3D | int | float):
            return NotImplemented
        if isinstance(other, int | float):
            return Point3D(self.x / other, self.y / other, self.z / other)
        return Point3D(self.x / other.x, self.y / other.y, self.z / other.z)

    def __floordiv__(self, other: Point3D | int | float):
        if not isinstance(other, Point3D | int | float):
            return NotImplemented
        if isinstance(other, int | float):
            return Point3D(self.x // other, self.y // other, self.z // other)
        return Point3D(self.x // other.x, self.y // other.y, self.z // other.z)

    def __mod__(self, other: Point3D | int | float):
        if not isinstance(other, Point3D | int | float):
            return NotImplemented
        if isinstance(other, int | float):
            return Point3D(self.x % other, self.y % other, self.z % other)
        return Point3D(self.x % other.x, self.y % other.y, self.z % other.z)

    def __pow__(self, other: Point3D | int | float):
        if not isinstance(other, Point3D | int | float):
            return NotImplemented
        if isinstance(other, int | float):
            return Point3D(self.x ** other, self.y ** other, self.z ** other)
        return Point3D(self.x ** other.x, self.y ** other.y, self.z ** other.z)

    def __pos__(self):
        return self

    def __neg__(self):
        return Point3D(-self.x, -self.y, -self.z)

    def __delattr__(self, item):
        raise NotImplementedError(f"Cannot delete attribute {item}")