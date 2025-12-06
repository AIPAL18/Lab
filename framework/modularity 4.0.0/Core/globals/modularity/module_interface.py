from abc import ABCMeta

type Any = object

__all__ = [
    "Interface",
    "ModuleInterface",
]


class Interface(ABCMeta): ...


class ModuleInterface(metaclass=Interface):
    @classmethod
    def interface(cls) -> type:
        assert hasattr(cls, "__interface"), "Not normal"
        return getattr(cls, "__interface")
    
    @classmethod
    def __init_subclass__(interface: type) -> None:
        def init_subclass(cls):
            setattr(cls, "__interface", interface)
            
        setattr(interface, "__init_subclass__", classmethod(init_subclass))


# Tests
if __name__ == "__main__":
    from abc import abstractmethod


    class IUiEngine(ModuleInterface):
        @abstractmethod
        def qmlEngine(self) -> object: ...

        @abstractmethod
        def quit(self) -> None: ...

        @abstractmethod
        def clearComponentCache(self) -> None: ...


    class UiEngine(IUiEngine):
        def qmlEngine(self) -> object:
            return object()
        
        def quit(self) -> None:
            pass

        def clearComponentCache(self) -> None:
            pass
    

    class VeryUiEngine(UiEngine):
        ...
    

    # print(dir(IUiEngine))
    # print(dir(UiEngine))

    engine = UiEngine()
    print(engine.interface())
    vengine = VeryUiEngine()
    print(vengine.interface())
    