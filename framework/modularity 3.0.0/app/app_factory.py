# Projet : Jeu-de-la-vie
# Auteurs : Elie RUGGIERO

from __future__ import annotations
from .internal.cmd_options import CmdOptions
from .internal.gui_app import GuiApp
from .internal.cli_app import ConsoleApp
from Core.globals.types import IApplication
from Core.ui.UiModule import UiModule

class AppFactory(object):
    __last_id = 0

    def __init__(self):
        super().__init__()
    
    def newApp(
            self: AppFactory,
            options: CmdOptions
    ) -> IApplication:
        if options.runMode == IApplication.RunMode.GuiApp:
            return self.__newGuiApp(options)
        else:
            return self.__newConsoleApp(options)
    
    def __newGuiApp(
            self: AppFactory,
            options: CmdOptions
    ) -> IApplication:
        self.__last_id += 1

        app = GuiApp(options)

        # Here
        # app.addModule(AppShellModule())
        app.addModule(UiModule())

        return app
    
    def __newConsoleApp(
            self: AppFactory,
            options: CmdOptions
    ) -> IApplication:
        ...
