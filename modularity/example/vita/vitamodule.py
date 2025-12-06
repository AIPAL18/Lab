from .ivitaservice import IVitaService
from modularity import ModuleSetup, ioc
from typing import override
from .internal.vitaservice import VitaService
from bind import proxy


class VitaModule(ModuleSetup):
    @override
    def moduleName() -> str:
        return "vita"
    
    @override
    def registerExports(self) -> None:
        service = proxy(VitaService(), IVitaService)
        ioc().registerExport(IVitaService, VitaModule.moduleName(), service)
