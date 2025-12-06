# Projet : Jeu-de-la-vie
# Auteurs : Elie RUGGIERO

from __future__ import annotations
from enum import Enum
from framework.globals.IApplication import IApplication
from typing import Optional

__all__ = [
    "CmdOptions",
]


class Ui(object):
    physicalDotsPerInch: Optional[float] = None


class App(object):
    revertToFactorySettings: Optional[bool] = None


class CmdOptions(object):
    class ParamKey(Enum):
        HighlightConfigPath = 0x01
        StylePath = 0x02
        ScoreSource = 0x03
        ScoreTransposeOptions = 0x04
        ForceMode = 0x05
        SoundProfile = 0x06
    
    runMode = IApplication.RunMode.GuiApp
    
    ui = Ui()
    app = App()
