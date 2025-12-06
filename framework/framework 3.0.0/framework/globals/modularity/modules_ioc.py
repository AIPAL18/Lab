# Projet : Jeu-de-la-vie
# Auteurs : Elie RUGGIERO

from __future__ import annotations
from typing import Optional
from .module_interface import (ModuleCreator, ModuleInterface, InterfaceInfo, 
                              ModuleExportCreator, InterfaceIdType)
from ..internal import Singleton
from .. import bind

type Any = object
 
__all__ = [
    "ModulesIoC",
    "Creator",
]


@Singleton
class ModulesIoC(object):
# private:
    class Service:
        def __init__(self, c: ModuleCreator | None, sourceModule: str, p: bind.BoundProxy[ModuleInterface]):
            assert isinstance(c, (ModuleCreator, type(None))), f"{c=}"
            assert isinstance(sourceModule, str), f"{sourceModule=}"
            assert bind.is_bound(p), f"{p=}"

            self.creator = c
            self.sourceModule = sourceModule
            self.pointer = p
    
        def __repr__(self) -> str:
            return f"<{ModulesIoC.Service.__module__}.{ModulesIoC.Service.__qualname__} (creator={self.creator!r}, module={self.sourceModule!r}, pointer={self.pointer!r})>"
    
    __map: dict[str, Service] = {}
    
    def _registerService(
            self: ModulesIoC,
            module: str,
            info: InterfaceInfo,
            p: Optional[bind.BoundProxy],
            c: Optional[ModuleCreator]
    ) -> None:
        
        foundIt = self.__map.get(info._id, None)
        if foundIt is not None:
            return

        self.__map[info._id] = self.Service(c, module, p)

    def _unregisterService(
            self: ModulesIoC,
            info: InterfaceInfo
    ) -> None:
        self.__map.pop(info._id)
    
    def _doResolvePtrByInfo(
            self: ModulesIoC,
            usageModule: str,
            info: InterfaceInfo,
            callInfo: str = ""
    ) -> Optional[bind.BoundProxy]:
        if info.internal:
            if usageModule != info.module:
                print("Assertion failed!! Interface '", info._id, "' is internal",
                      ", usage module: '", usageModule, "'",
                      ", interface module: '", info.module, "'",
                      ", called from: ", "unknown" if len(callInfo) == 0 else callInfo)
                return
        
        from pprint import pprint
        pprint(self.__map)
        inj: ModulesIoC.Service = self.__map.get(info._id, None)
        
        if inj is None:
            return None
        if inj.pointer:
            return inj.pointer
        if inj.creator:
            return inj.creator
        
        return None

# public:
    # Register Export

    def registerExportCreator(
            self: ModulesIoC, 
            interface: InterfaceIdType,
            module: str, 
            creator: ModuleCreator
    ) -> None:
        assert isinstance(module, str)
        assert isinstance(creator, ModuleCreator)
        
        if not creator:
            return

        self._registerService(
            module, 
            interface.interfaceInfo(), 
            None,
            creator
        )
    
    def registerExport(
            self: ModulesIoC,
            interface: InterfaceIdType,
            module: str,
            p: bind.BoundProxy
    ) -> None:
        assert isinstance(module, str), f"{module=}"
        assert bind.is_bound(p), f"{p=}"
        assert isinstance(p, interface), f"{p=}"
        
        self._registerService(module, interface.interfaceInfo(), p, None)
    
    # Register Internal
    def registerInternalCreator(
            self: ModulesIoC,
            interface: InterfaceIdType,
            module: str,
            creator: ModuleCreator
    ) -> None:
        assert isinstance(module, str), f"{module = }"
        assert isinstance(creator, ModuleCreator)
    
        if not creator:
            return creator
        
        self._registerService(
            module, 
            interface.interfaceInfo(), 
            None, 
            creator
        )
    
    def registerInternal(
            self: ModulesIoC,
            interface: InterfaceIdType,
            module: str,
            p: bind.BoundProxy | Any
        ) -> None:
        assert isinstance(module, str), f"{module = }"
        assert isinstance(p, interface), f"{p=}"
        assert bind.is_bound(p), f"{p=}"
        
        if not p:
            return
        
        self._registerService(module, interface.interfaceInfo(), p, None)
    
    # Unregister
    def unregister(
            self: ModulesIoC,
            interface: InterfaceIdType,
            _: str  # module, TODO: understand why we ask for this arg if we don't use it anyway
    ) -> None:
        self._unregisterService(interface.interfaceInfo())
    
    def unregisterIfRegistered(
            self: ModulesIoC,
            interface: InterfaceIdType,
            module: str,
            p: bind.BoundProxy
    ) -> None:
        assert isinstance(module, str), f"{module = }"
        assert bind.is_bound(p), f"{p=}"
        assert isinstance(p, interface), f"{p=}"
        
        if self.resolve[interface](module, str()) == p:
            self.unregister[interface](module)
    
    # Resolve
    def resolve(
            self: ModulesIoC,
            interface: InterfaceIdType,
            module: str,
            callInfo: str,
    ) -> Optional[bind.BoundProxy]:
        assert isinstance(module, str), f"{module = }"
        assert isinstance(callInfo, str), f"{callInfo = }"
        
        return self._doResolvePtrByInfo(module, interface.interfaceInfo(), callInfo)

    def resolveRequiredImport(
            self: ModulesIoC,
            interface: InterfaceIdType,
            module: str
    ) -> Optional[bind.BoundProxy]:
        assert isinstance(module, str), f"{module = }"

        _p = self._doResolvePtrByInfo(module, interface.interfaceInfo())
        if not _p:
            print("not found implementation for interface:", interface.interfaceInfo())

        return _p
        
    def reset(self: ModulesIoC):
        self.__map.clear()


class Creator[T: ModuleInterface](ModuleExportCreator):
    def base(self):
        # TODO: get ride of this methode
        self.__orig_class__.args[0]
    
    def create(self) -> bind.BoundProxy[ModuleInterface]:
        print("Check the behavior of Create.create()")
        return bind.bind(None, self.base())
