# Projet : Jeu-de-la-vie
# Auteurs : Elie RUGGIERO

from __future__ import annotations
from framework.globals import std
from .internal.cmd_options import CmdOptions
from .internal.gui_app import GuiApp
from .internal.cli_app import ConsoleApp
from new_source.app.IApplication import IApplication

class AppFactory(object):
    __last_id = 0

    def __init__(self):
        super.__init__()
    
    def newApp(
            self: AppFactory,
            options: CmdOptions
    ) -> std.shared_ptr[IApplication]:
        if options.runMode == IApplication.RunMode.GuiApp:
            return self.__newGuiApp(options)
        else:
            return self.__newConsoleApp(options)
    
    def __newGuiApp(
            self: AppFactory,
            options: CmdOptions
    ) -> std.shared_ptr[IApplication]:
        self.__last_id += 1

        app: GuiApp = std.make_shared(GuiApp(options))

        # Here
        app.addModule(AppShellModule())

        return app
    
    def __newConsoleApp(
            self: AppFactory,
            options: CmdOptions
    ) -> std.shared_ptr[IApplication]:
        ...
