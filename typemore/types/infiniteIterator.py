class InfiniteIterator:
    """An integer range iterator that can run forever, with optional bounds and step.

        When end is None, the iterator is unbounded: each call to next() yields
        the current value and advances, forever. When end is given, iteration
        stops before reaching end, matching the behavior of range().

        The step can be negative, in which case the iterator counts downward and
        stops before reaching end.

        Example:
            >>> list(InfiniteIterator(1, 3))
            [1, 2]

            >>> it = InfiniteIterator(0, step=2)
            >>> next(it), next(it), next(it)
            (0, 2, 4)

            >>> list(InfiniteIterator(5, 1, -1))
            [5, 4, 3, 2]
        """
    def __init__(self, start: int, end: int = None, step: int = None):
        if not isinstance(start, int) or not isinstance(end, int | None) or not isinstance(step, int | None):
            raise TypeError("InfiniteIterator arguments must be integers")
        self.start = start
        self.end = end
        self.step = step

    def __iter__(self):
        return self

    def __next__(self):
        if self.end is None:
            value = self.start
            if self.step is None:
                self.start += 1
            else:
                self.start += self.step
            return value

        if self.step is not None and self.step < 0:
            if self.start <= self.end:
                raise StopIteration
        else:
            if self.start >= self.end:
                raise StopIteration
        value = self.start
        if self.step is None:
            self.start += 1
        else:
            self.start += self.step
        return value