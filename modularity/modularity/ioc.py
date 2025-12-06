# Projet : Jeu-de-la-vie
# Auteurs : Elie RUGGIERO

from __future__ import annotations
from .modules_ioc import ModulesIoC
import threading
from .. import bind

__all__ = [
    "Inject",
    "ioc",
]


def ioc() -> ModulesIoC:
    return ModulesIoC.instance()


class Inject[I: type]:

    # @classmethod
    # def __class_getitem__(cls, item):
    #     # https://docs.python.org/3/reference/datamodel.html#object.__class_getitem__
    #     if not isinstance(item, Iterable):
    #         return GenericAlias(cls, item)
    #     else:
    #         raise TypeError("An object cannot be of several types at the same time")
    
    def __init__(
            self: Inject, 
            module: I
    ) -> None:
        super().__init__()
        self.__module: str = module.__name__
        self.__base: type = module
        self.__interface: I = None
    
    def base(self: Inject) -> type:
        return self.__base
    
        # if hasattr(self, "__orig_class__"):
        #     base = self.__orig_class__.__args__[0]
        #     if isinstance(base, TypeVar):
        #         return base.__default__
        #     else:
        #         return base
        # else:
        #     return NoneType
    
    def get(self: Inject) -> bind.BoundProxy[I]:
        if not self.__interface:
            mutex = threading.Lock()
            with mutex:
                if not self.__interface:
                    self.__interface = ioc().resolve(self.__module, "", self.base())
        
        return self.__interface
    
    def set(
            self: Inject,
            impl: I
    ) -> None:
        self.__interface = impl
    
    def __call__(self, *args, **kwds) -> bind.BoundProxy[I]:
        return self.get()
