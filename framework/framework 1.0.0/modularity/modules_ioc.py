from __future__ import annotations
from typing import TypeVar, overload
from module_interface import (ModuleCreator, ModuleInterface, InterfaceInfo, 
                              ModuleExportCreator)
import std

I = TypeVar("I")

__all__ = [
    "ModulesIoC",
    "Creator",
]


class ModulesIoC(object):
    class Service:
        def __init__(self, c: ModuleCreator, sourceModule: str, p: std.shared_ptr[ModuleInterface]):
            self.c = c
            self.sourceModule = sourceModule
            self.p = p
    
    __map: dict[str: Service]
    
    def __new__(cls):
        """
        Pattern Singleton
        """
        if hasattr(cls, "instance"):
            cls.instance = super().__new__(cls)
        
        return cls.instance
    
    @classmethod
    def instance(cls) -> ModulesIoC:
        """
        Pattern Singleton
        """
        return cls.__new__(cls)
    
    # Register Export
    def registerExportCreator(
            self: ModulesIoC, 
            module: str, 
            creator: std.ptr[ModuleCreator]
    ) -> None:
        if not creator:
            return

        self._registerService(
            module, 
            creator.interfaceInfo(), 
            std.shared_ptr[ModuleInterface](),
            creator
        )
    
    @overload
    def registerExport(
            self: ModulesIoC,
            module: str,
            p: std.Optionalptr[I]
    ) -> None:
        if not p:
            return
        self.registerExport(module, std.make_shared(p))
    
    def registerExportNoDelete(
            self: ModulesIoC,
            module: str,
            p: I
    ) -> None:
        return NotImplemented
    
    @overload
    def registerExport(
            self: ModulesIoC,
            module: str,
            p: std.shared_ptr[I]
    ) -> None:
        if not p:
            return
        
        self._registerService(module, p.interfaceInfo(), p, std.nullptr())  # None ?
    
    # Register Internal
    def registerInternalCreator(
            self: ModulesIoC,
            module: str,
            creator: ModuleCreator
    ) -> None:
        if not creator:
            return creator
        
        self._registerService(
            module, 
            creator.interfaceInfo(), 
            std.shared_ptr(), 
            creator
        )
    
    @overload
    def registerInternal(
            self: ModulesIoC,
            module: str,
            p: std.ptr[I]
        ) -> None:
        if not p:
            return
        
        self.registerInternal(module, std.make_shared[p])
    
    def registerInternalNoDelete(
            self: ModulesIoC,
            module: str,
            p: std.ptr[I]
    ) -> None:
        return NotImplemented
    
    @overload
    def registerInternal(
            self: ModulesIoC,
            module: str,
            p: std.shared_ptr[I]
    ) -> None:
        if not p:
            return
        
        self._registerService(module, p.interfaceInfo(), p, std.nullptr())
    
    # Unregister
    def unregister(
            self: ModulesIoC,
            module: str,  #! TODO: replace with _
            p: std.shared_ptr[I]
    ) -> None:
        self._unregisterService(p.interfaceInfo())
    
    def unregisterIfRegistered(
            self: ModulesIoC,
            module: str,
            p: std.shared_ptr[I]
    ) -> None:
        if self.resolve(module, str(), p) == p:
            self.unregister(module, p)
    
    # Resolve
    def resolve(
            self: ModulesIoC,
            module: str,
            callInfo: str,
            p: std.shared_ptr[I]
    ) -> std.shared_ptr:
        _p = self._doResolvePtrByInfo(module, p.interfaceInfo(), callInfo)
        return std.make_shared[ModuleInterface](_p)

    def resolveRequiredImport(
            self: ModulesIoC,
            module: str,
            p: std.shared_ptr[I]
    ) -> std.shared_ptr:
        _p = self._doResolvePtrByInfo(module, p.interfaceInfo(), str())
        if not _p:
            print("not found implementation for interface:", p.interfaceInfo().id)
        return std.make_shared[ModuleInterface](_p)
        
    def reset(self: ModulesIoC):
        self.__map.clear()
    
# Private

    def _unregisterService(
            self: ModulesIoC,
            info: InterfaceInfo
    ) -> None:
        self.__map.pop(info.id)
    
    def _registerService(
            self: ModulesIoC,
            module: str,
            info: InterfaceInfo,
            p: std.shared_ptr,
            c: std.ptr
    ) -> None:
        foundIt = self.__map.get(info.id, None)
        if foundIt is None:
            return

        self.__map[info.id] = self.Service(module, c, p)
    
    def _doResolvePtrByInfo(
            self: ModulesIoC,
            usageModule: str,
            info: InterfaceInfo,
            callInfo: str
    ) -> None:
        if info.internal:
            if usageModule != info.module:
                print("Assertion failed!! Interface '", info.id, "' is internal",
                      ", usage module: '", usageModule, "'",
                      ", interface module: '", info.module, "'",
                      ", called from: ", "unknown" if len(callInfo) == 0 else callInfo)
                return
                
        inj = self.__map.get(info.id, None)
        if inj is None:
            return std.nullptr()
        if inj.p:
            return inj.p
        # TODO: Check !!!
        if inj.c:
            return inj.c
        
        return std.nullptr()


class Creator(ModuleExportCreator):
    def create(t: type) -> std.shared_ptr:
        return std.make_shared[t]()
