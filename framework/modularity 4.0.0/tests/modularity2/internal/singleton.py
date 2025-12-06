from __future__ import annotations

from functools import partial
from typing import Self

__all__ = [
    "Singleton",
]

# class SingletonInterface[T](ABC):
#     @deprecated("Not sure enough to use it.")
#     @classmethod
#     @abstractmethod
#     def instance(cls) -> T: ...


def Singleton[T](cls: T) -> T: # | SingletonInterface[T]:
    new = partial(cls.__new__)

    def new_helper(*args, **kwds):
        if not hasattr(cls, "__instance"):
            # cls.__instance = new(*args, **kwds)
            setattr(cls, "__instance", new(*args, **kwds))
        return getattr(cls, "__instance")
    
    def init_subclass(*args, **kwds):
        # TODO: rewrite this error
        raise TypeError("It is impossible to inherit from a Singleton class")
    
    cls.__new__ = new_helper
    cls.__init_subclass__ = init_subclass

    # @classmethod
    # def instance(cls: type[T]) -> T:
    #     assert hasattr(cls, f"__instance"), f"{cls.__name__} must be instantiated before attempting to retrieve its instance."
    
    #     return cls.__instance

    # # cls.instance = instance
    # setattr(cls, "instance", instance)

    return cls


if __name__ == "__main__":
    @Singleton
    class A:
        def __new__(cls, var) -> Self:
            print(f"New A {var=}")
            return super().__new__(cls)
        
        def __init__(self, var) -> None:
            print(f"Init A with {var=}")
            self.var = var
        
        def __call__(self, *args, **kwds) -> None:
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
    print(f"{A.__instance is a = }")
