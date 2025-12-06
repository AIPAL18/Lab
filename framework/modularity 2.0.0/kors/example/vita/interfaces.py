from __future__ import annotations
from framework.globals.modularity import INTERFACE_ID, ModuleExportInterface
from abc import abstractmethod

__all__ = [
    "IVitaService",
]

@INTERFACE_ID
class IVitaService(ModuleExportInterface):
    def __init__(self: IVitaService) -> None:
        super().__init__()
    
    @abstractmethod
    def doSomeThing(self: IVitaService) -> str: ...
    
    @abstractmethod
    def doSomeThingWithAlpha(self: IVitaService) -> str: ...
