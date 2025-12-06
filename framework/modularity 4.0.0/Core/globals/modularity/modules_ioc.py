# Projet : Jeu-de-la-vie
# Auteurs : Elie RUGGIERO

from __future__ import annotations
from typing import Any, Self, Optional
from .module_interface import ModuleInterface
from ..internal import Singleton

__all__ = [
    "ModulesIoC",
]


@Singleton
class ModulesIoC(object):
    __map: dict[ModuleInterface, object] = {}
    
    def register(
            self: ModulesIoC,
            impl: ModuleInterface,
            instance: object
    ) -> None:
        self.__map[impl.interface()] = instance
    
    def unregister(
            self: ModulesIoC,
            interface: ModuleInterface
    ) -> None:
        self.__map.pop(interface)
    
    def unregisterIfRegistered(
            self: ModulesIoC,
            interface: ModuleInterface
    ) -> None:
        if interface in self.__map:
            self.__map.pop(interface)

    def resolve[I: ModuleInterface](
            self: ModulesIoC,
            interface: type[I]
    ) -> I:
        return self.__map[interface]

    def resolveIfRegistered[I: ModuleInterface](
            self: ModulesIoC,
            interface: type[I]
    ) -> Optional[I]:
        return self.__map.get(interface, None)
        
    def reset(self: ModulesIoC):
        self.__map.clear()
    
    def __call__(self) -> Self:
        """
        Retrocompatibilité avec ioc comme fonction.
        """
        return self
