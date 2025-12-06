# Projet : Jeu-de-la-vie
# Auteurs : Elie RUGGIERO

from __future__ import annotations
from typing import Generic, TypeVar
from types import NoneType
from .modules_ioc import ModulesIoC
import threading
from .. import std

T = TypeVar("T")
I = TypeVar("I")

__all__ = [
    "Inject",
    "ioc",
]


def ioc() -> ModulesIoC:
    return ModulesIoC.instance()


class Inject(Generic[I]):
    @classmethod
    def __class_getitem__(cls: Inject, key: type):
        # https://docs.python.org/3/reference/datamodel.html#object.__class_getitem__
        cls.__cls_type = key
        return super().__class_getitem__(key)

    @classmethod
    def class_type(cls: Inject) -> type:
        # Private members: 
        # https://www.geeksforgeeks.org/private-attributes-in-a-python-class/
        if hasattr(cls, f"_{Inject.__name__}__type"):
            return cls.__cls_type
        return NoneType

    def __new__(
            cls: Inject,
            module: type = NoneType
        ) -> None:
        if not hasattr(cls, f"_{Inject.__name__}__cls_type"):
            cls.__cls_type = module

        
        #! TODO: it's only working if __new__ is done right after 
        # __class_getitem__, otherwise, types could not match 
        # (__class_getitem__ could be called in between)
        instance = super().__new__(cls)
        instance.__type = cls.__cls_type
        # Reset __cls_type
        cls.__cls_type = NoneType
        
        return instance
    
    __module: str
    __interface: std.shared_ptr = std.nullptr()
    
    def __init__(
            self: Inject, 
            module: type = NoneType
    ) -> None:
        super().__init__()
        # __module is "NoneType"
        self.__module = module.__name__
    
    def type(self: Inject) -> type:
        return self.__type
    
    def get(self: Inject) -> std.shared_ptr[I]:
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
