# typemore

A collection of custom Python data types for specialized behavior.

## Install

```bash
pip install typemore
```

## Usage

```python
from typemore import StrictFloat, Range, Interval

StrictFloat(0.1) + StrictFloat(0.2)   # StrictFloat:0.3

3 in Range(1, 5)                      # True

Interval(True, 1, 5, False)           # [1, 5)
```

## Types

- `StrictFloat` — a float subclass that does arithmetic with Decimal
- `Range` — a closed numeric interval
- `Interval` — an interval with open or closed endpoints
- `Point2D` / `Point3D` / `PointAnyD` — points with element-wise operations
- `Auto` — a wrapper that forwards operations and supports most type-conversion functions without raising
- `Debug` — a debugging wrapper that prints what happens
- `ChainNode` — a linked-list node
- `InfiniteIterator` — an integer range iterator that can run forever
- `ReadOnlyBox` — a read-only wrapper
- `DisplayProxy` — a proxy that separates display behavior from real behavior
- `LenLimit` — enforces a maximum length on a container
- `TimeLimit` — expires after a given amount of time
- `MemLimit` — enforces a maximum memory size on a container

## License

MIT