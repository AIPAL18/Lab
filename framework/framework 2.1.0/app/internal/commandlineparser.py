# Projet : Jeu-de-la-vie
# Auteurs : Elie RUGGIERO

from __future__ import annotations
from PySide6.QtCore import (
    QCommandLineParser, QCommandLineOption, QCoreApplication)
from .cmd_options import CmdOptions
from ..IApplication import IApplication

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
        args = prepareArguments(argc, argc)
        self._parser.parse(args)

        # Parse custom args

    
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
    #     if arg.startswith("-debugger"):
    #         continue

    #     arguments.append(arg)
    
    # return arguments
    return [arg for arg in argv if not arg.startswith("-debugger")]


def internalCommandLineOption(*args) -> QCommandLineOption:
    """
    

    Args:
    Returns:
    """
    option = QCommandLineOption(*args)
    option.setFlags(QCommandLineOption.Flag.HiddenFromHelp)
    return option


if __name__ == "__main__":
    argc = 2
    argv = ["coucou", "-debugger bonjour"]
    
    print(prepareArguments(argc, argv))
