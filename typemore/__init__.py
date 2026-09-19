from .types.range import Range
from .types.point2D import Point2D
from .types.point3D import Point3D
from .types.pointAnyD import PointAnyD
from .types.auto import Auto
from .types.debug import Debug
from .types.strictFloat import StrictFloat
from .types.interval import Interval
from .types.chainNode import ChainNode
from .types.infiniteIterator import InfiniteIterator
from .types.readOnlyBox import ReadOnlyBox
from .types.displayProxy import DisplayProxy
from .types.lenLimit import LenLimit, LenLimitError
from .types.timeLimit import TimeLimit, TimeLimitError
from .types.memLimit import MemLimit, MemLimitError

__version__ = "0.1.1"
__author__ = "MCmaoshen"
__all__ = ["Range",
           "Point2D",
           "Point3D",
           "PointAnyD",
           "Auto",
           "Debug",
           "StrictFloat",
           "Interval",
           "ChainNode",
           "InfiniteIterator",
           "ReadOnlyBox",
           "DisplayProxy",
           "LenLimit",
           "LenLimitError",
           "TimeLimit",
           "TimeLimitError",
           "MemLimit",
           "MemLimitError"]

__error__ = [
    "LenLimitError",
    "TimeLimitError",
    "MemLimitError"
]

def doc():
    print(
        f"name: {__name__}\n"
        f"version: {__version__}\n"
        f"author: {__author__}\n"
        f"public types: {len(__all__) - len(__error__)}\n"
        f"errors types: {len(__error__)}"
    )