# Projet : Jeu-de-la-vie
# Auteurs : Elie RUGGIERO

from __future__ import annotations
from abc import ABC, abstractmethod
from . import moduleName
from bind import Bound
from functools import cache

__all__ = [
    "Interface",
    "ModuleInterface",
    "ModuleExportInterface",
    "ModuleInternalInterface",
    "ModuleCreator",
    "ModuleExportCreator",
    "ModuleInternalCreator",
    "InterfaceInfo",
    "Interface_Id",
    "InterfaceIdType",
]

class Interface(ABC):
    @staticmethod
    @abstractmethod
    def isInternalInterface() -> bool: ...


class ModuleInterface(Interface): ...


class ModuleExportInterface(ModuleInterface):
    @staticmethod
    def isInternalInterface() -> bool:
        return False


class ModuleInternalInterface(ModuleInterface):
    @staticmethod
    def isInternalInterface() -> bool:
        return True


class ModuleCreator(Interface):
    @abstractmethod
    def create() -> Bound[ModuleCreator]: ...


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
        assert isinstance(i, str), f"{i=}"
        assert isinstance(m, str), f"{m=}"
        assert isinstance(intr, bool), f"{intr=}"
        self.id = i
        self.module = m
        self.internal = intr
    
    def __repr__(self):
        return f"<{InterfaceInfo.__name__} id={self.id}, module={self.module}, internal={self.internal}>"


class InterfaceIdTemplate:
    @abstractmethod
    def interfaceInfo() -> InterfaceInfo: ...


type InterfaceIdType[T] = T | InterfaceIdTemplate


def Interface_Id[T: Interface](interface: T) -> T:
    @cache
    @staticmethod
    def interfaceInfo() -> InterfaceInfo:
        return InterfaceInfo(
            interface.__name__, 
            moduleName(interface), 
            interface.isInternalInterface()
        )

    setattr(interface, "interfaceInfo", interfaceInfo)

    return interface


if __name__ == "__main__":
    @Interface_Id
    class Foo(ModuleExportInterface):
        def bar(self):
            print("bar !")
