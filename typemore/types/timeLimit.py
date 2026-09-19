import time
from typing import Literal

class TimeLimitError(TimeoutError):
    pass

class TimeLimit:
    """A wrapper that expires after a given amount of time.

        TimeLimit wraps a value and records the time of construction. Attribute
        reads, method calls, string conversion, and representation all raise
        TimeLimitError once the limit has passed. The value itself is not copied
        or modified.

        The limit is fixed at construction time. The unit argument accepts 'ms',
        's', 'min', or 'h', and defaults to 's'. The limit is stored internally
        in seconds.

        Example:
            >>> tl = TimeLimit([1, 2, 3], 1)
            >>> tl.append(4)
            >>> time.sleep(2)
            >>> tl.append(5)
            TimeLimitError: time limit exceeded: object expired after 1 seconds
        """
    def __init__(self, value, limit: int | float, unit: Literal['ms', 's', 'min', 'h'] = 's'):
        if not isinstance(limit, int | float):
            raise TypeError(f"time limit must be an int or float, not {type(limit).__name__!r}")
        self._value = value
        if unit == 'ms':
            self._limit = limit / 1000
        elif unit == 's':
            self._limit = limit
        elif unit == 'min':
            self._limit = limit * 60
        elif unit == 'h':
            self._limit = limit * 3600
        else:
            raise ValueError(f"unknown unit: {unit!r}")
        self._time = time.time()

    def _check(self):
        if time.time() - self._time >= self._limit:
            raise TimeLimitError(
                f"time limit exceeded: object expired after {self._limit} seconds"
            )

    def __getattr__(self, name):
        if name.startswith('_'):
            raise AttributeError(name)
        self._check()
        attr = getattr(self._value, name)
        if callable(attr):
            def wrapper(*args, **kwargs):
                self._check()
                return attr(*args, **kwargs)
            return wrapper
        return attr

    def __str__(self):
        self._check()
        return str(self._value)

    def __repr__(self):
        self._check()
        return f"TimeLimit({self._value!r}, limit={self._limit})"