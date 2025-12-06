# Projet : Jeu-de-la-vie
# Auteurs : Elie RUGGIERO

"""
# modularity


"""

__all__ = [
    # func_info
    "classFunc",
    "className",
    "funcSig",
    "funcName",
    "moduleName",

    # ioc
    "Inject",
    "ioc",

    # module_interface
    "ModuleInterface",
    "ModuleExportInterface",
    "ModuleInternalInterface",
    "ModuleCreator",
    "ModuleExportCreator",
    "ModuleInternalCreator",
    "InterfaceInfo",
    "INTERFACE_ID",

    # module_setup
    "ModuleSetup",

    #modules_ioc
    "ModulesIoC",
]

from .func_info import (classFunc, className, funcSig, funcName, moduleName)
from .ioc import (Inject, ioc)
from .module_interface import (
    ModuleInterface, ModuleExportInterface, ModuleInternalInterface, 
    ModuleCreator, ModuleExportCreator, ModuleInternalCreator, InterfaceInfo, 
    INTERFACE_ID
)
from .module_setup import (ModuleSetup)
from .modules_ioc import (ModulesIoC)
