from __future__ import annotations
from framework.globals.modularity import ModuleSetup, ioc, moduleName
from typing import override
from .internal.vita_service import VitaService


__all__ = [
    "VitaModule",
]


class VitaModule(ModuleSetup):
    @override
    def moduleName(self) -> str:
        return "vita"
    
    @override
    def registerExports(self) -> None:
        ioc().registerExport(moduleName(self), VitaService())
