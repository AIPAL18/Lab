# Projet : Jeu-de-la-vie
# Auteurs : Elie RUGGIERO

from __future__ import annotations
from abc import ABC, abstractmethod

__all__ = [
    "ModuleSetup",
]


class ModuleSetup(ABC):
    @abstractmethod
    def moduleName(self: ModuleSetup) -> str: ...
    
    def registerExports(self) -> None: pass
    
    def resolveImports(self) -> None: pass
    
    def registerResources(self) -> None: pass
    
    def registerUiTypes(self) -> None: pass
    
    def onPreInit(self) -> None: pass
    
    def onInit(self) -> None: pass
    
    def onAllInited(self) -> None: pass
    
    def onDelayedInit(self) -> None: pass
    
    def onDeinit(self) -> None: pass

    def onDestroy(self) -> None: pass
    
    def onStartApp(self) -> None: pass
