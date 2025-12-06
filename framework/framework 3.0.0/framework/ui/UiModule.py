from __future__ import annotations

from framework.globals.modularity import ModuleSetup, ioc
from framework.globals.types.IApplication import IApplication
from .internal.UiEngine import UiEngine
from framework.globals import bind

from typing import override


class UiModule(ModuleSetup):
    @override
    @staticmethod
    def moduleName() -> str:
        return "ui"

    @override
    def registerExports(self) -> None:
        self.__uiengine = bind.proxy(UiEngine(), UiEngine)
        ioc().registerExport(UiEngine, module=self.moduleName(), p=self.__uiengine)

    @override
    def resolveImports(self) -> None:
        ...

    @override
    def registerApi(self) -> None:
        ...

    @override
    def registerResources(self) -> None:
        ... 

    @override
    def registerUiTypes(self) -> None:
        ...

    @override
    def onPreInit(self, mode: IApplication.RunMode) -> None:
        ...

    @override
    def onInit(self, mode: IApplication.RunMode) -> None:
        ...

    @override
    def onAllInited(self, mode: IApplication.RunMode) -> None:
        self.__uiengine.init()

    @override
    def onDeinit(self) -> None:
        ...

