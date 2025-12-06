# Projet : Jeu-de-la-vie
# Auteurs : Elie RUGGIERO

from __future__ import annotations

if __name__ == "__main__":
    import os, sys
    sys.path.insert(0, os.path.abspath("."))
    print(sys.path)

from abc import ABCMeta, abstractmethod
from Core.globals.modularity.func_info import moduleName
from functools import cache

type Any = object

__all__ = [
    "Implementation",
    "InterfaceInfo",
    "Interface",
    "ModuleInterface",
]

type Implementation[T] = T | Interface


class InterfaceInfo:
    name: str
    module: str
    interface: type
    
    def __init__(self, _name: str, _module: str, _inter: type):
        assert isinstance(_name, str), f"{_name=}"
        assert isinstance(_module, str), f"{_module=}"
        assert isinstance(_inter, type), f"{_module=}"
        self.name = _name
        self.module = _module
        self.interface = _inter
    
    def __repr__(self):
        return f"<{InterfaceInfo.__name__} name={self.name !r}, module={self.module !r}, interface={self.interface !r}>"


def isabstract(cls: type) -> bool:
    if not hasattr(cls, '__abstractmethods__'):
        return False
    return len(cls.__abstractmethods__) > 0


def isinterface(cls: type, **kwds: Any) -> bool:
    if "interface" in kwds and kwds["interface"] is True:
        return True
    
    if isinstance(cls, InterfaceMeta) and isabstract(cls):
        return True
    
    return False


class InterfaceMeta(ABCMeta):
    def __new__(cls, name: str, bases: tuple[type, ...], namespace: dict[str, Any], /, **kwds: Any):
        instance = super(InterfaceMeta, cls).__new__(cls, name, bases, namespace)
        
        if isinterface(instance, **kwds):
            @cache
            @staticmethod
            def interfaceInfo() -> InterfaceInfo:
                return InterfaceInfo(
                    instance.__name__, 
                    moduleName(instance),
                    instance, 
                )

            setattr(instance, "__interface__", True)
            setattr(instance, "interfaceInfo", interfaceInfo)
        else:
            @cache
            @staticmethod
            def interfaceInfo() -> InterfaceInfo:
                # NOTE: Liskov Substitution Principle violation !
                # raise AttributeError(f"type object '{name}' has no attribute 'interfaceInfo'")
                return instance.__base__.interfaceInfo()
            
            if hasattr(instance, "__interface__"):
                setattr(instance, "__interface__", False)
        
        setattr(instance, "interfaceInfo", interfaceInfo)
        return instance


class Interface(metaclass=InterfaceMeta, interface=True):
    @staticmethod
    @abstractmethod
    def interfaceInfo() -> InterfaceInfo: ...


class ModuleInterface(Interface, interface=True): ...


if __name__ == "__main__":
    class IFoo(Interface, interface=True):
        @abstractmethod
        def bar(self): ...
    
    class Foo(IFoo):
        def bar(self):
            print("bar !")
    

    foo = Foo()
    print(f"{Foo.interfaceInfo() == IFoo.interfaceInfo() = }")
    print(f"{IFoo.interfaceInfo() = }")
    print(f"{Foo.interfaceInfo()  = }")
    