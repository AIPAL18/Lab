from __future__ import annotations

from functools import partial

__all__ = [
    "Singleton",
]


def Singleton[T](cls: T) -> T:
    new = partial(cls.__new__)

    def new_helper(*args, **kwds) -> T:
        if not hasattr(cls, f"__instance"):
            cls.__instance = new(*args, **kwds)
        return cls.__instance
    
    def init_subclass(*args, **kwds):
        # TODO: rewrite this error
        raise TypeError("It is impossible to inherit from a Singleton class")
    
    cls.__new__ = new_helper
    cls.__init_subclass__ = init_subclass


    @classmethod
    def instance(cls: type[T]) -> T:
        return cls()

    cls.instance = instance

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

    try:
        class B(A):
            def __init__(self, var):
                super().__init__(var)
    except BaseException as exception:
        print(exception)
    
    a = A("a")
    b = A("b")
    
    print(f"{a is b = }\n{a.var, b.var = }")
    print(f"{A.instance() is a = }")
