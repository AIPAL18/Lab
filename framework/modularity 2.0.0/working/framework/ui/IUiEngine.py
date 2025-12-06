from __future__ import annotations
from framework.globals.modularity import INTERFACE_ID, ModuleExportInterface
from abc import ABC, abstractmethod
from PySide6.QtQml import QQmlApplicationEngine, QQmlEngine


@INTERFACE_ID
class IUiEngine(ModuleExportInterface):
    @abstractmethod
    def updateTheme(self) -> None: ...

    @abstractmethod
    def qmlAppEngine(self) -> QQmlApplicationEngine: ...

    @abstractmethod
    def qmlEngine(self) -> QQmlEngine: ...

    @abstractmethod
    def quit(self) -> None: ...

    @abstractmethod
    def clearComponentCache(self) -> None: ...

    # @abstractmethod
    # def graphicsApi(self) -> GraphicsApiProvider.Api: ...

    # @abstractmethod
    # def graphicsApiName(self) -> str: ...

    @abstractmethod
    def addSourceImportPath(self, path: str) -> None: ...

