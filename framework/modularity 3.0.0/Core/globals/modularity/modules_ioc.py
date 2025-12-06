# Projet : Jeu-de-la-vie
# Auteurs : Elie RUGGIERO

from __future__ import annotations
from typing import Optional
from .module_interface import (ModuleInterface, InterfaceInfo, 
                            Interface, Implementation)
from ..internal import Singleton

type Any = object

__all__ = [
    "ModulesIoC",
]


@Singleton
class ModulesIoC(object):
# private:
    class Service:
        def __init__(self, module: str, impl: ModuleInterface):
            assert isinstance(module, str), f"{module=}"
            assert isinstance(impl, Interface), f"{impl=}"

            self.module = module
            self.implementation = impl
    
        def __repr__(self) -> str:
            return f"<{ModulesIoC.Service.__module__}.{ModulesIoC.Service.__qualname__} (module={self.module!r}, implementation={self.implementation!r})>"
    
    __map: dict[str, Service] = {}
    
    def _registerService(
            self: ModulesIoC,
            module: str,
            info: InterfaceInfo,
            impl: Implementation,
    ) -> None:
        assert info.name not in self.__map, f"{info.name} already registed !"
        print(info)
        self.__map[info.name] = self.Service(module, impl)

    def _unregisterService(
            self: ModulesIoC,
            info: InterfaceInfo
    ) -> None:
        self.__map.pop(info.name)
    
    def _doResolveImplByInfo(
            self: ModulesIoC,
            module: str,  # can be used in case of name's overloading
            info: InterfaceInfo
    ) -> Optional[Implementation]:
        inj: ModulesIoC.Service = self.__map.get(info.name, None)

        if inj is None:
            return None
        if inj.implementation:
            return inj.implementation
        
        return None

# public:
    def register(
            self: ModulesIoC,
            interface: Interface,
            module: str,
            p: Implementation
    ) -> None:
        assert isinstance(module, str), f"{module=}"
        assert isinstance(p, Interface), f"{p=}"
        assert isinstance(p, interface), f"{p=}"
        
        self._registerService(module, interface.interfaceInfo(), p)
    
    def unregister(
            self: ModulesIoC,
            interface: Interface
    ) -> None:
        assert issubclass(interface, Interface), f"{interface=}"

        self._unregisterService(interface.interfaceInfo())
    
    def unregisterIfRegistered(
            self: ModulesIoC,
            interface: Interface,
            module: str,
            p: Implementation
    ) -> None:
        assert issubclass(interface, Interface), f"{interface=}"
        assert isinstance(module, str), f"{module = }"
        assert isinstance(p, Interface), f"{p=}"
        assert isinstance(p, interface), f"{p=}"
        
        if self.resolve[interface](module, str()) == p:
            self.unregister[interface](module)

    def resolve(
            self: ModulesIoC,
            interface: Interface,
            module: str,
            callInfo: str,
    ) -> Optional[Implementation]:
        assert issubclass(interface, Interface), f"{interface=}"
        assert isinstance(module, str), f"{module = }"
        assert isinstance(callInfo, str), f"{callInfo = }"
        
        return self._doResolveImplByInfo(module, interface.interfaceInfo())

    def resolveRequiredImport(
            self: ModulesIoC,
            interface: Interface,
            module: str
    ) -> Optional[Implementation]:
        assert issubclass(interface, Interface), f"{interface=}"
        assert isinstance(module, str), f"{module = }"

        _p = self._doResolveImplByInfo(module, interface.interfaceInfo())
        if not _p:
            print("not found implementation for interface:", interface.interfaceInfo())

        return _p
        
    def reset(self: ModulesIoC):
        self.__map.clear()
