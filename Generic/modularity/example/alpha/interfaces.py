from __future__ import annotations
from framework.globals.modularity import INTERFACE_ID, ModuleExportInterface
from abc import abstractmethod

__all__ = [
    "IAlphaService",
]


@INTERFACE_ID
class IAlphaService(ModuleExportInterface):
    def __init__(self: IAlphaService) -> None:
        super().__init__()
    
    @abstractmethod
    def info(self: IAlphaService) -> str: ...
