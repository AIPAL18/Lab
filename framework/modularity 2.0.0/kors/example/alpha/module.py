from __future__ import annotations
from framework.globals.modularity import ModuleSetup, ioc, moduleName
from typing import override
from .internal.alpha_service import AlphaService

__all__ = [
    "AlphaModule",
]


class AlphaModule(ModuleSetup):
    def __init__(self: AlphaModule):
        super().__init__()
    
    @override
    def moduleName(self: AlphaModule) -> str:
        return "alpha"
    
    @override
    def registerExports(self) -> None:
        ioc().registerExport(moduleName(self), AlphaService())

