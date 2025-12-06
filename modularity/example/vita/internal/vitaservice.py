from ..ivitaservice import IVitaService
from typing import override
from modularity import Inject
from alpha.ialphaservice import IAlphaService


class VitaService(IVitaService):
    def __init__(self):
        self.alphaService = Inject(IAlphaService)
    
    @override
    def do_some_thing(self) -> str:
        return "vita_service_data"

    @override
    def do_some_thing_with_alpha(self) -> str:
        return f"vita_service_data_{self.alphaService().info()}"
