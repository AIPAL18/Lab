from __future__ import annotations
from framework.globals.modularity import Inject, ModuleSetup
from .vita.interfaces import IVitaService


class App(object):
    def __new__(cls, *args, **kwds):
        if not hasattr(cls, f"_{cls.__name__}__instance"):
            cls.__instance = object.__new__(cls, *args, **kwds)
        
        return cls.__instance

    def __init__(self: App):
        self.vitaService = Inject[IVitaService]()
        
        self.__modules: list[ModuleSetup] = []

    def addModule(
            self: App,
            module: ModuleSetup
    ) -> None:
        self.__modules.append(module)

    def run(
            self: App,
            argc: int,
            argv: list[str]
    ) -> int:
        for m in self.__modules:
            m.registerExports()

        for m in self.__modules:
            m.resolveImports()
            m.registerResources()
            m.registerUiTypes()
            m.onPreInit()
        
        for m in self.__modules:
            m.onInit()
        
        for m in self.__modules:
            m.onAllInited()
        
        # Run
        
        data: str = self.vitaService().doSomeThing()
        print(data)
        data2: str = self.vitaService().doSomeThingWithAlpha()
        print(data2)

        # End
    
        for m in self.__modules:
            m.onDeinit()
        
        for m in self.__modules:
            m.onDestroy()
        
        return 0
        