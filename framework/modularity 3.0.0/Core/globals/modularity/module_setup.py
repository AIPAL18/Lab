# Projet : Jeu-de-la-vie
# Auteurs : Elie RUGGIERO

from __future__ import annotations
from abc import ABC, abstractmethod
from ..types.IApplication import IApplication

__all__ = [
    "ModuleSetup",
]


class ModuleSetup(ABC):
    @staticmethod
    @abstractmethod
    def moduleName() -> str: ...
    
    def registerExports(self: ModuleSetup) -> None: pass
    
    def resolveImports(self: ModuleSetup) -> None: pass
    
    def registerResources(self: ModuleSetup) -> None: pass
    
    def registerUiTypes(self: ModuleSetup) -> None: pass
    
    def onPreInit(self: ModuleSetup, mode: IApplication.RunMode) -> None: pass
    
    def onInit(self: ModuleSetup, mode: IApplication.RunMode) -> None: pass
    
    def onAllInited(self: ModuleSetup, mode: IApplication.RunMode) -> None: pass
    
    def onDelayedInit(self: ModuleSetup) -> None: pass
    
    def onDeinit(self: ModuleSetup) -> None: pass

    def onDestroy(self: ModuleSetup) -> None: pass
    
    def onStartApp(self: ModuleSetup) -> None: pass
