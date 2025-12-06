# Python 3.12+ (PEP 695)

from __future__ import annotations
from typing import TypeVar, Iterable, ClassVar, Self, Optional
from types import GenericAlias, NoneType

type Any = object


class ProxyType[T]:
    __obj: T

    def __new__(cls, obj) -> Self:
        inst = super().__new__(cls)
        inst.__obj = obj

        return inst
    
    def get(self) -> T:
        return self.__obj
    
    def __eq__(self, value) -> bool:
        return self.__obj == value
        
    def __getattr__(self, attr: str) -> Any:
        return self.__obj.__getattribute__(attr)

    def __repr__(self) -> str:
        return f"<{ProxyType.__module__}.{ProxyType.__qualname__} ({self.__obj})>"

    __hash__: ClassVar[None]  # type: ignore[assignment]


proxy = ProxyType


class ReferenceType[T]:
    __obj: T
    
    def __new__(cls, obj: Optional[T] = None, /) -> Self:
        inst = super().__new__(cls)

        assert obj is not None
        
        inst.__obj = obj
        return inst
    
    def __call__(self) -> T:
        return self.__obj
    
    def base(self) -> type:
        if hasattr(self, "__orig_class__"):
            base = self.__orig_class__.__args__[0]
            if isinstance(base, TypeVar):
                return type(self.__obj)
            else:
                return base
        else:
            return type(self.__obj)

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
