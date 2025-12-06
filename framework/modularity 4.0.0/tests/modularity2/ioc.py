from __future__ import annotations
from .modules_ioc import ModulesIoC
import threading

__all__ = [
    "Inject",
    "ioc",
]


# def ioc() -> ModulesIoC:
#     return ModulesIoC()

ioc = ModulesIoC()  # Une instance coûte moins chère qu'un appelle de fonction.


class Inject[I: type]:
    # TODO: rework it all
    def __init__(self: Inject, module: I) -> None:
        super().__init__()
        self.__module: str = module.__name__
        self.__base: type = module
        self.__interface: I = None
    
    def base(self: Inject) -> type:
        return self.__base
    
    def get(self: Inject) -> I:
        if not self.__interface:
            mutex = threading.Lock()
            with mutex:
                if not self.__interface:
                    self.__interface = ioc().resolve(self.__module, "", self.base())
        
        return self.__interface
    
    def set(self: Inject, impl: I) -> None:
        # NOTE: When is it used ? And what for ?
        self.__interface = impl
    
    def __call__(self) -> I:
        return self.get()
