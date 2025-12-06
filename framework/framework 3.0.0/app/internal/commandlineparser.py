# Projet : Jeu-de-la-vie
# Auteurs : Elie RUGGIERO

from __future__ import annotations
from PySide6.QtCore import (
    QCommandLineParser, QCommandLineOption, QCoreApplication)
from .cmd_options import CmdOptions
from framework.globals.types.IApplication import IApplication, BaseApplication
from config import *

__all__ = [
    "CommandLineParser",
]


class CommandLineParser(object):
    _parser = QCommandLineParser()
    _options = CmdOptions()
    
    def __init__(self: CommandLineParser) -> None:
        super().__init__()
    
    def init(self: CommandLineParser):
        self._parser.addHelpOption()  # -?, -h, --help
        self._parser.addVersionOption()  # -v, --version

        self.__opts = {
            "long-version": 
                QCommandLineOption(["long-version", "lv"], "Print detailed version information"),
            "debug": 
                QCommandLineOption(["d", "debug"], "Debug mode"),
            "cli":
                QCommandLineOption(["cli", "console"], "Console Application Mode"),
        }

        for opt in self.__opts.values():
            self._parser.addOption(opt)

    def parse(
            self: CommandLineParser,
            argc: int,
            argv: list[str]
        ) -> None:
        """
        Parse the command line arguments for further processing.
        
        Args:
            self (CommandLineParser):
            argc (int):
                Number of arguments contained in `argv`. (C++ legacy)
            argv (list[int]):
                List of command-line arguments.
        Returns:
            out (None):
                In-place modification.
        """
        args = prepareArguments(argc, argv)
        self._parser.parse(args)

        # Parse custom args
        
        if self._parser.isSet(self.__opts["long-version"]):
            printLongVersion()
            exit(0)
        
        if self._parser.isSet(self.__opts["cli"]):
            self._options.runMode = IApplication.RunMode.ConsoleApp

    
    def processBuiltinArgs(
            self: CommandLineParser,
            app: QCoreApplication
        ) -> None:
        #! NOTE: some options require an instance of QCoreApplication
        self._parser.process(app)

    def runMode(self: CommandLineParser) -> IApplication.RunMode:
        return self._options.runMode

    def options(self: CommandLineParser) -> CmdOptions:
        return self._options


def prepareArguments(argc: int, argv: list[str]) -> list[str]:
    """
    Prepare arguments and return them.

    Args:
        argc (int):
            Number of arguments contained in `argv`. (C++ legacy)
        argv (list[int]):
            List of command-line arguments.
    Returns:
        argv (list[int]):
            Prepared arguments.
    """
    # arguments: list[str] = []
    # for i in range(argc):
    #     arg = argv[i]
    #     if arg.startswith("-qmljsdebugger"):
    #         continue

    #     arguments.append(arg)
    
    # return arguments
    return [arg for arg in argv if not arg.startswith("-qmljsdebugger")]


def internalCommandLineOption(*args) -> QCommandLineOption:
    """
    

    Args:
    Returns:
    """
    option = QCommandLineOption(*args)
    option.setFlags(QCommandLineOption.Flag.HiddenFromHelp)
    return option


def printLongVersion():
    if BaseApplication.appUnstable():
        print(f"{APP_TITLE}: {APP_DESCRIPTION}\nUnstable Prerelease for Version {BaseApplication.appVersion()}; Build {BaseApplication.appRevision()}")


if __name__ == "__main__":
    argc = 2
    argv = ["coucou", "-qmljsdebugger bonjour"]
    
    print(prepareArguments(argc, argv))
