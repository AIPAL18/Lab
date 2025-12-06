# Projet : Jeu-de-la-vie
# Auteurs : Elie RUGGIERO

from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TypeVar
from framework.globals.modularity import moduleName
from .. import std

T = TypeVar("T")

__all__ = [
    "ModuleInterface",
    "ModuleExportInterface",
    "ModuleInternalInterface",
    "ModuleCreator",
    "ModuleExportCreator",
    "ModuleInternalCreator",
    "InterfaceInfo",
    "INTERFACE_ID",
]


class ModuleInterface(ABC): ...


class ModuleExportInterface(ModuleInterface):
    @staticmethod
    def isInternalInterface() -> bool:
        return False


class ModuleInternalInterface(ModuleInterface):
    @staticmethod
    def isInternalInterface() -> bool:
        return True


class ModuleCreator(ABC):
    @abstractmethod
    def create() -> std.shared_ptr[ModuleCreator]: ...


class ModuleExportCreator(ModuleCreator):
    @staticmethod
    def isInternalInterface() -> bool:
        return False


class ModuleInternalCreator(ModuleCreator):
    @staticmethod
    def isInternalInterface() -> bool:
        return True


class InterfaceInfo:
    id: str
    module: str
    internal: bool = False
    def __init__(self, i: str, m: str, intr: bool):
        self.id = i
        self.module = m
        self.internal = intr


class INTERFACE_ID(object):
    def __new__(cls, interface: T) -> T:
        def interfaceInfo(*arg, **kwds):
            return InterfaceInfo(
                interface, 
                moduleName(interface), 
                interface.isInternalInterface()
            )

        interface.interfaceInfo = interfaceInfo

        return interface
