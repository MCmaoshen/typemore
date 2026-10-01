import sys
from functools import wraps

def private(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        caller_qualname = sys._getframe(1).f_code.co_qualname
        method_qualname = func.__qualname__
        parent = method_qualname[:method_qualname.rfind('.')]

        if not caller_qualname.startswith(parent):
            raise RuntimeError(f"{method_qualname} is private")
        return func(*args, **kwargs)
    return wrapper