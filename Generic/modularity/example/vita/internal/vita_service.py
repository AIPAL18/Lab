from __future__ import annotations
from ..interfaces import IVitaService
from framework.globals.modularity import Inject
from typing import override
from ...alpha.interfaces import IAlphaService


class VitaService(IVitaService):
    def __init__(self):
        super().__init__()
        self.alphaService = Inject[IAlphaService]()
    
    @override
    def doSomeThing(self: VitaService) -> str:
        return "vita_service_data"

    @override
    def doSomeThingWithAlpha(self: VitaService) -> str:
        return "vita_service_data_" + self.alphaService().info()
