from abc import abstractmethod
from modularity import Interface_Id, ModuleExportInterface


@Interface_Id
class IAlphaService(ModuleExportInterface):
    @abstractmethod
    def info(self) -> str: ...
