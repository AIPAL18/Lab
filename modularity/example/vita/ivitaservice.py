from abc import abstractmethod
from modularity import Interface_Id, ModuleExportInterface


@Interface_Id
class IVitaService(ModuleExportInterface):
    @abstractmethod
    def do_some_thing(self) -> str: ...

    @abstractmethod
    def do_some_thing_with_alpha(self) -> str: ...
