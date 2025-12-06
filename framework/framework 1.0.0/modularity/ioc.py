from __future__ import annotations
from typing import Generic, TypeVar
from types import NoneType
from .modules_ioc import ModulesIoC
import threading
import std
T = TypeVar("T")
I = TypeVar("I")

__all__ = [
    "Inject",
]


class Inject(Generic[T]):
    _interface: std.ptr = std.nullptr()
    _module: str
     
    def __init__(self: Inject, module: str = "") -> None:
        super().__init__()
        self._module = module
    
    def get(self: Inject) -> std.shared_ptr:
        if self._interface is std.nullptr():
            mutex = threading.Lock()
            with mutex:
                if not m_i:
                    m_i = ioc().resolve(I, self._module)
        return self._interface


def ioc() -> ModulesIoC:
    return ModulesIoC.instance()


class Inject(Generic[I]):
    @classmethod
    def __class_getitem__(cls: Inject, key):
        # https://docs.python.org/3/reference/datamodel.html#object.__class_getitem__
        cls.__type = key
        return super().__class_getitem__(key)

    @classmethod
    def type(cls) -> type:
        # Private members: 
        # https://www.geeksforgeeks.org/private-attributes-in-a-python-class/
        if hasattr(cls, f"_{Inject.__name__}__type"):
            return cls.__type
        return NoneType
    
    __module: str
    __interface: std.shared_ptr = std.nullptr()
    
    def __init__(
            self: Inject, 
            module: str = "",
    ) -> None:
        super().__init__()
        self.__module = module
    
    def get(self: Inject) -> std.shared_ptr:
        if not self.__interface:
            mutex = threading.Lock()
            with mutex:
                if not self.__interface:
                    self.__interface = ioc().resolve(self.__module, "", self.type())
        
        return self.__interface
    
    def set(
            self: Inject,
            impl: std.shared_ptr
    ) -> None:
        self.__interface = impl
    
    def __call__(self, *args, **kwds) -> I:
        return self.get().get()
