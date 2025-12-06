from modularity import Inject, ModuleSetup
from vita.ivitaservice import IVitaService


class App:
    def __init__(self):
        self.vita_service: Inject[IVitaService] = Inject(IVitaService)
        self._modules: list[ModuleSetup] = []
    
    def add_module(self, module: ModuleSetup) -> None:
        self._modules.append(module)
    

    def run(self) -> int:
        for m in self._modules:
            m.registerExports()
        
        for m in self._modules:
            m.resolveImports()
            m.registerResources()
            m.registerUiTypes()
            m.onPreInit()
        
        for m in self._modules:
            m.onInit()
        
        for m in self._modules:
            m.onAllInited()
        
        # NOTE: running app for real (until # end)
        
        data: str = self.vita_service().do_some_thing()
        print(f"vita data : {data!a}")
        data2: str = self.vita_service().do_some_thing_with_alpha()
        print(f"vita data (with alpha) : {data2!r}")
        
        # end

        for m in self._modules:
            m.onDeinit()
        
        for m in self._modules:
            m.onDestroy()
        
        return 0
