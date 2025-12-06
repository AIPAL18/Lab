# Projet : Jeu-de-la-vie
# Auteurs : Elie RUGGIERO

from __future__ import annotations
from abc import abstractmethod
from ..framework.globals.modularity import ModuleExportInterface, INTERFACE_ID
from .appshell_types import StartupModeType
from ..framework.globals.types import Ret
from ..framework.globals.asynchronous import Notification  #! TODO: implement it
from pathlib import Path


@INTERFACE_ID
class IAppShellConfiguration(ModuleExportInterface):
    def __init__(self):
        super().__init__()
    
    @abstractmethod
    def hasCompletedFirstLaunchSetup() -> bool: ...

    @abstractmethod
    def setHasCompletedFirstLaunchSetup(has: bool) -> None: ...

    @abstractmethod
    def startupModeType() -> StartupModeType: ...

    @abstractmethod
    def setStartupModeType(type: StartupModeType) -> None: ...

    @abstractmethod
    def startupScorePath() -> Path: ...

    @abstractmethod
    def setStartupScorePath(scorePath: Path) -> None: ...

    @abstractmethod
    def userDataPath() -> Path: ...

    @abstractmethod
    def handbookUrl() -> str: ...

    @abstractmethod
    def askForHelpUrl() -> str: ...

    @abstractmethod
    def museScoreUrl() -> str: ...

    @abstractmethod
    def museScoreForumUrl() -> str: ...

    @abstractmethod
    def museScoreContributionUrl() -> str: ...

    @abstractmethod
    def musicXMLLicenseUrl() -> str: ...

    @abstractmethod
    def musicXMLLicenseDeedUrl() -> str: ...

    @abstractmethod
    def museScoreVersion() -> str: ...

    @abstractmethod
    def museScoreRevision() -> str: ...

    @abstractmethod
    def isNotationNavigatorVisible() -> bool: ...

    @abstractmethod
    def setIsNotationNavigatorVisible(visible: bool) -> None: ...

    @abstractmethod
    def isNotationNavigatorVisibleChanged() -> Notification: ...

    @abstractmethod
    def needShowSplashScreen() -> bool: ...

    @abstractmethod
    def setNeedShowSplashScreen(show: bool) -> None: ...

    @abstractmethod
    def startEditSettings() -> None: ...

    @abstractmethod
    def applySettings() -> None: ...

    @abstractmethod
    def rollbackSettings() -> None: ...

    @abstractmethod
    def revertToFactorySettings(keepDefaultSettings: bool = False, notifyAboutChanges: bool = True) -> None: ...

    @abstractmethod
    def  sessionProjectsPaths() -> list[Path]: ...
    
    @abstractmethod
    def setSessionProjectsPaths(paths: list[Path]) -> Ret: ...
