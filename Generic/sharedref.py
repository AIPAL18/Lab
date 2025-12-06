# Python 3.12+ (PEP 695)

from __future__ import annotations
from typing import TypeVar, Iterable, Self, ClassVar
from types import GenericAlias, NoneType

type Any = object


class ProxyType[T: type = NoneType]:
    __obj: T

    def __new__(cls, obj) -> Self:
        inst = super().__new__(cls)
        inst.__obj = obj

        return inst
        
    def __getattr__(self, attr: str) -> Any:
        return self.__obj.__getattribute__(attr)

    def __repr__(self) -> str:
        return f"<{ProxyType.__module__}.{ProxyType.__qualname__} ({self.__obj})>"

    __hash__: ClassVar[None]  # type: ignore[assignment]


class ReferenceType[T: type = NoneType]:
    __obj: T
    
    def __new__(cls, obj: T = NoneType, /) -> Self:
        inst = super().__new__(cls)
        if obj is NoneType:
            inst.__obj = None
        else:
            inst.__obj = obj
    
    def __call__(self) -> T:
        return self.__obj
    
    def base(self) -> type:
        if hasattr(self, "__orig_class__"):
            base = self.__orig_class__.__args__[0]
            if isinstance(base, TypeVar):
                return base.__default__
            else:
                return base
        else:
            return NoneType

    def get(self) -> T:
        return self.__call__()
    
    def __eq__(self, value: object, /) -> bool:
        return self.__obj == value
        
    def __hash__(self) -> int:
        return self.__obj.__hash__()

    def __class_getitem__(cls, item: Any, /) -> GenericAlias:
        # https://docs.python.org/3/reference/datamodel.html#object.__class_getitem__
        if not isinstance(item, Iterable):
            return GenericAlias(cls, item)
        else:
            raise TypeError("An object cannot be of several types at the same time")


ref = ReferenceType


if __name__ == "__main__":
    # import weakref, gc

    class A(list): ...

    def helper(self: Self) -> Any:
        print("\t", self.__callback__, type(self))
        
        return None
    

    # obj = A(["ele 0"])
    # ref_ = weakref.ref(obj, helper)
    # print(obj, ref_(), sep="\n", end="\n\n")
    # ref_().append("ele 1")
    # print(obj, ref_(), sep="\n", end="\n\n")
    # print(type(ref_))

    # del obj
    # gc.collect()

    obj = A(["ele 0"])
    ref_ = ProxyType(obj)
    print(obj, ref_, sep="\n", end="\n\n")
    ref_.append("ele 1")
    print(obj, ref_, sep="\n", end="\n\n")
    print(type(ref_))
    
