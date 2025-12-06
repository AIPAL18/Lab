# Projet : Jeu-de-la-vie
# Auteurs : Elie RUGGIERO

from __future__ import annotations
from core.globals import bind
from .internal.cmd_options import CmdOptions
from .internal.gui_app import GuiApp
from .internal.cli_app import ConsoleApp
from core.globals.types.IApplication import IApplication
from core.ui.UiModule import UiModule

class AppFactory(object):
    __last_id = 0

    def __init__(self):
        super().__init__()
    
    def newApp(
            self: AppFactory,
            options: CmdOptions
    ) -> bind.BoundProxy[IApplication]:
        if options.runMode == IApplication.RunMode.GuiApp:
            return self.__newGuiApp(options)
        else:
            return self.__newConsoleApp(options)
    
    def __newGuiApp(
            self: AppFactory,
            options: CmdOptions
    ) -> bind.BoundProxy[IApplication]:
        self.__last_id += 1

        app = GuiApp(options)

        # Here
        # app.addModule(AppShellModule())
        app.addModule(UiModule())

        return app
    
    def __newConsoleApp(
            self: AppFactory,
            options: CmdOptions
    ) -> bind.BoundProxy[IApplication]:
        self.__last_id += 1
        return bind.bind(None, IApplication)
