from __future__ import  annotations

class PointerNone:
    pass

point_none = PointerNone()

class ChainNode:
    """
    A singly linked list node whose class also inherits from type(value).

        Each instance stores a value and a pointer to the next node. The class
        of an instance is generated dynamically based on the type of value, so
        a node can also use the methods and operators of its underlying type.
        For example, ChainNode(5) inherits from int, and ChainNode("a") inherits
        from str.

        The end of a chain is marked by point_none, a sentinel instance of
        PointerNone. Use "pointer is point_none" to test for the end.
        """
    _cache = {}

    def __new__(cls, value, pointer = point_none):
        base = type(value)
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
        if value is None or base is bool:
            instance = super().__new__(new_cls)
            return instance
        elif issubclass(base, (int, float, str, tuple, frozenset, bytes)):
            instance= base.__new__(new_cls, value)
            return instance
        else:
            instance = base.__new__(new_cls)
        return instance

    def __init__(self, value, pointer = point_none):
        self.value = value
        self.pointer = pointer

    def __repr__(self) -> str:
        return f"Pointer({self.value}, {self.pointer if self.pointer is not point_none else ''})"

    def __str__(self) -> str:
        return f"({self.value}, {self.pointer if self.pointer is not point_none else ''})"

    def getvalue_number(self, number: int):
        """
        Return the value of the node at index number, where 0 is self.

        Raises ValueError if number is not a non-negative int, and IndexError
        if the chain ends before reaching that index.
        """
        if not isinstance(number, int) or number < 0:
            raise ValueError("index out of range")
        node = self
        for _ in range(number):
            if not isinstance(node.pointer, ChainNode):
                raise IndexError("index out of range")
            node = node.pointer
        return node.value

    def getpointer_number(self, number: int):
        """
        Return the node at index number, where 0 is self.

        Raises ValueError if number is not a non-negative int, and IndexError
        if the chain ends before reaching that index.
        """
        if not isinstance(number, int) or number < 0:
            raise ValueError("index out of range")
        node = self
        for _ in range(number):
            if not isinstance(node.pointer, ChainNode):
                raise IndexError("index out of range")
            node = node.pointer
        return node

    def getpointer_value(self, value):
        """
        Return the pointer of the first node whose value equals value.

        Raises ValueError if no such node exists.
        """
        node = self._find_node(value)
        if node is None:
            raise ValueError("value not found in chain")
        return node.pointer

    def setpointer_number(self, number: int, pointer) -> None:
        """
        Set the pointer of the node at index number, where 0 is self.

        Raises ValueError if number is not a non-negative int, and IndexError
        if the chain ends before reaching that index.
        """
        if not isinstance(number, int) or number < 0:
            raise ValueError("index out of range")
        node = self
        for _ in range(number):
            if not isinstance(node, ChainNode):
                raise IndexError("index out of range")
            node = node.pointer
        if not isinstance(node, ChainNode):
            raise IndexError("index out of range")
        node.pointer = pointer

    def setpointer_value(self, value, pointer) -> None:
        """
        Set the pointer of the first node whose value equals value.

        Raises ValueError if no such node exists.
        """
        node = self._find_node(value)
        if node is None:
            raise ValueError("value not found in chain")
        node.pointer = pointer

    def setvalue_number(self, number: int, value) -> None:
        """
        Set the value attribute of the node at index number, where 0 is self.

        For immutable subclasses such as ChainNode[int], the instance's own
        numeric value does not change; only the value attribute is updated.
        Raises ValueError if number is not a non-negative int, and IndexError
        if the chain ends before reaching that index.
        """
        if not isinstance(number, int) or number < 0:
            raise ValueError("index out of range")
        node = self
        for _ in range(number):
            if not isinstance(node, ChainNode):
                raise IndexError("index out of range")
            node = node.pointer
        if not isinstance(node, ChainNode):
            raise IndexError("index out of range")
        node.value = value

    def delete_number(self, number: int):
        """
        Delete the node at index number.

        If number is 0, return the next node as the new head. Otherwise, return
        self. Raises ValueError if number is not a non-negative int, and
        IndexError if the chain ends before reaching that index.
        """
        if not isinstance(number, int) or number < 0:
            raise ValueError("index out of range")

        if number == 0:
            if not isinstance(self.pointer, ChainNode):
                raise IndexError("index out of range")
            return self.pointer

        prev = self
        for _ in range(number - 1):
            if not isinstance(prev.pointer, ChainNode):
                raise IndexError("index out of range")
            prev = prev.pointer

        target = prev.pointer
        if not isinstance(target, ChainNode):
            raise IndexError("index out of range")
        prev.pointer = target.pointer
        return self

    def delete_value(self, value):
        """
        Delete the first node whose value equals value.

        Return the new head. When the deleted node is the head, the successor
        becomes the new head. Raises ValueError if no such node exists.
        """
        if self.value == value:
            if not isinstance(self.pointer, ChainNode):
                raise ValueError("value not found in chain")
            return self.pointer

        prev = self
        cur = self.pointer
        while isinstance(cur, ChainNode):
            if cur.value == value:
                prev.pointer = cur.pointer
                return self
            prev = cur
            cur = cur.pointer
        raise ValueError("value not found in chain")

    def node_search(self, value) -> int:
        """
        Return the index of the first node whose value equals value.

        Index 0 is self. Raises ValueError if no such node exists.
        """
        if self.value == value:
            return 0
        pointer_save = self
        pointer_now = self.pointer
        i = 1
        while True:
            if not isinstance(pointer_now, ChainNode):
                if pointer_now == value and pointer_now == pointer_save.value:
                    return i
                else:
                    raise ValueError(f"{value} not found in chain")
            if pointer_now.value == value:
                return i
            pointer_now = pointer_now.pointer
            pointer_save = pointer_save.pointer
            i += 1

    def _find_node(self, value):
        """Return the first node whose value equals value, or None."""
        node = self
        while isinstance(node, ChainNode):
            if node.value == value:
                return node
            node = node.pointer
        return None

    def node_len(self, value=point_none, pointer=point_none) -> int:
        """
        Return the number of nodes starting after a given position.

        With no argument, count nodes after self. With pointer=xxx, count
        starting at xxx (inclusive). With value=xxx, count starting after the
        node holding xxx. The two keyword arguments are mutually exclusive.
        """
        if pointer is not point_none and value is not point_none:
            raise ValueError("pointer and value are mutually exclusive")

        if value is not point_none:
            node = self._find_node(value)
            if node is None:
                raise ValueError(f"value {value} not found in chain")
            start = node.pointer
        elif pointer is not point_none:
            start = pointer
        else:
            start = self.pointer

        i = 0
        while isinstance(start, ChainNode):
            start = start.pointer
            i += 1
        return i

    def deep_len(self, value=point_none, pointer=point_none) -> int:
        """
        Return the depth of a node relative to self.

        Positive if the node comes after self, 0 if it is self, negative if it
        comes before self. The two keyword arguments are mutually exclusive.
        Raises ValueError if the node is not on the same chain.
        """
        if pointer is not point_none and value is not point_none:
            raise ValueError("pointer and value are mutually exclusive")

        if value is not point_none:
            node = self._find_node(value)
            if node is None:
                raise ValueError(f"value {value} not found in chain")
        elif pointer is not point_none:
            node = pointer
        else:
            raise ValueError("either pointer or value is required")

        cur = self
        depth = 0
        while isinstance(cur, ChainNode):
            if cur is node:
                return depth
            cur = cur.pointer
            depth += 1

        cur = node
        depth = 0
        while isinstance(cur, ChainNode):
            if cur is self:
                return -depth
            cur = cur.pointer
            depth += 1

        raise ValueError("the two nodes are not in the same chain")