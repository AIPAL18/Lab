from __future__ import annotations

from typing import TypeVar
from functools import partial

T = TypeVar("T")


def Singleton(cls: T) -> T:
    new = partial(cls.__new__)

    def new_helper(*args, **kwds):
        if not hasattr(cls, f"__instance"):
            cls.__instance = new(*args, **kwds)
        return cls.__instance

    def init_subclass(*args, **kwds):
        # TODO: rewrite this error
        raise TypeError("It is impossible to inherit from a Singleton class")

    cls.__new__ = new_helper
    cls.__init_subclass__ = init_subclass
    return cls


if __name__ == "__main__":
    @Singleton
    class A:
        def __new__(cls, var):
            print(f"New A {var=}")
            return super().__new__(cls)
        
        def __init__(self, var):
            print(f"Init A with {var=}")
            self.var = var
        
        def __call__(self, *args, **kwds):
            print(args, kwds)

    class B(A):
        def __init__(self, var):
            super().__init__(var)
    
    a = A("a")
    b = A("b") 
    
    print(f"{a is b = }\n{a.var, b.var}")
