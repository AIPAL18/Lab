# Projet : Jeu-de-la-vie
# Auteurs : Elie RUGGIERO

from __future__ import annotations
from abc import abstractmethod
from Core.globals.modularity import (
    ModuleInterface, ModulesIoC, ioc)
from Core.globals.types.version import Version
from typing import override
from PySide6.QtGui import QWindow
from PySide6.QtCore import QObject, QEvent, QCoreApplication, QProcess
from PySide6.QtGui import QGuiApplication
from config import *
from enum import IntEnum


class IApplication(ModuleInterface):
    class RunMode(IntEnum):
        GuiApp = 0x00
        ConsoleApp = 0x01
    
    @abstractmethod
    def name(self: IApplication) -> str: ...

    @abstractmethod
    def unstable(self: IApplication) -> bool: ...

    @abstractmethod
    def version(self: IApplication) -> Version: ...

    @abstractmethod
    def fullVersion(self: IApplication) -> Version: ...

    @abstractmethod
    def build(self: IApplication) -> str: ...

    @abstractmethod
    def revision(self: IApplication) -> str: ...

    @abstractmethod
    def runMode(self: IApplication) -> RunMode: ...

    @abstractmethod
    def noGui(self: IApplication) -> bool: ...

    @abstractmethod
    def perform(self: IApplication) -> None: ...

    @abstractmethod
    def finish(self: IApplication) -> None: ...

    @abstractmethod
    def restart(self: IApplication) -> None: ...

    @abstractmethod
    def ioc(self: IApplication) -> ModulesIoC: ...

    @abstractmethod
    def focusWindow(self: IApplication) -> QWindow: ...

    @abstractmethod
    def notify(self: IApplication, object: QObject, event: QEvent) -> bool: ...

    @abstractmethod
    def addModule(self: IApplication, module: object) -> None: ...


class BaseApplication(IApplication):
    def __init__(self):
        super().__init__()
        self.__runMode: IApplication.RunMode = IApplication.RunMode.GuiApp

    @staticmethod
    def appName() -> str:
        return APP_NAME

    @staticmethod
    def appTitle() -> str:
        return APP_TITLE

    @staticmethod
    def appUnstable() -> bool:
        return APP_UNSTABLE

    @staticmethod
    def appVersion() -> Version:
        return Version(APP_VERSION)

    @staticmethod
    def appFullVersion() -> Version:
        return BaseApplication.appVersion()

    @staticmethod
    def appBuild() -> str:
        return APP_BUILD_MODE

    @staticmethod
    def appRevision() -> str:
        return APP_REVISION

    @override
    def name(self: BaseApplication) -> str:
        return self.appName()

    def title(self: BaseApplication) -> str:
        return self.appTitle()

    @override
    def unstable(self: BaseApplication) -> bool:
        return self.appUnstable()

    @override
    def version(self: BaseApplication) -> Version:
        return self.appVersion()

    @override
    def fullVersion(self: BaseApplication) -> Version:
        return self.appFullVersion()

    @override
    def build(self: BaseApplication) -> str:
        return self.appBuild()

    @override
    def revision(self: BaseApplication) -> str:
        return self.appRevision()

    def setRunMode(self: BaseApplication, mode: IApplication.RunMode) -> None:
        self.__runMode = mode

    @override
    def runMode(self: BaseApplication) -> IApplication.RunMode:
        return self.__runMode

    @override
    def noGui(self: BaseApplication) -> bool:
        match self.__runMode:
            case self.RunMode.GuiApp:
                return False
            case self.RunMode.ConsoleApp:
                return True
        
        # default
        return False

    @override
    def restart(self: BaseApplication) -> None:
        program = QCoreApplication.instance().arguments()[0] # type: ignore

        # NOTE: remove the first argument - the program name
        arguments = QCoreApplication.instance().arguments()[1:] # type: ignore

        QCoreApplication.exit()

        QProcess.startDetached(program, arguments)

    @override
    def ioc(self: BaseApplication) -> ModulesIoC:
        return ioc()

    @override
    def focusWindow(self: BaseApplication) -> QWindow:
        return QGuiApplication.focusWindow()

    @override
    def notify(self: BaseApplication, object: QObject, event: QEvent) -> bool:
        return QGuiApplication.instance().notify(object, event) # type: ignore
