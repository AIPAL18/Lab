from __future__ import annotations
from abc import ABC, abstractmethod

__all__ = [
    "ModuleSetup",
]


class ModuleSetup(ABC):
    @abstractmethod
    def moduleName(self: ModuleSetup) -> str:
        ...
    
    @abstractmethod
    def registerExports(self) -> None: ...
    
    @abstractmethod
    def resolveImports(self) -> None: ...
    
    @abstractmethod
    def registerResources(self) -> None: ...
    
    @abstractmethod
    def registerUiTypes(self) -> None: ...
    
    @abstractmethod
    def onPreInit(self) -> None: ...
    
    @abstractmethod
    def onInit(self) -> None: ...
    
    @abstractmethod
    def onAllInited(self) -> None: ...
    
    @abstractmethod
    def onDelayedInit(self) -> None: ...
    
    @abstractmethod
    def onDeinit(self) -> None: ...

    @abstractmethod
    def onDestroy(self) -> None: ...
    
    @abstractmethod
    def onStartApp(self) -> None: ...
