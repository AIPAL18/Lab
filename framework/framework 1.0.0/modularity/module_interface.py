from __future__ import annotations
from abc import ABC, abstractmethod
from func_info import moduleName
import std
from typing import _Alias

__all__ = [
    "ModuleInterface",
    "ModuleExportInterface",
    "IModuleInternalInterface",
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


class IModuleInternalInterface(ModuleInterface):
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


def INTERFACE_ID(obj: object) -> None:
    """
    decorator ?
    """
    obj.info = InterfaceInfo(obj, moduleName(obj), obj.isInternalInterface())

