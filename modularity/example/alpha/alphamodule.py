from .ialphaservice import IAlphaService
from modularity import ModuleSetup, ioc
from typing import override
from .internal.alphaservice import AlphaService
from bind import proxy

class AlphaModule(ModuleSetup):
    @override
    def moduleName() -> str:
        return "alpha"
    
    @override
    def registerExports(self) -> None:
        service = proxy(AlphaService(), IAlphaService)
        ioc().registerExport(IAlphaService, AlphaModule.moduleName(), service)