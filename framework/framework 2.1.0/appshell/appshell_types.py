# Projet : Jeu-de-la-vie
# Auteurs : Elie RUGGIERO

from __future__ import annotations
from enum import Enum

__all__ = [
    "StartupModeType",
]


class StartupModeType(Enum):
    StartEmpty = 0x01
    ContinueLastSession = 0x02
    StartWithNewScore = 0x03
    StartWithScore = 0x04
    Recovery = 0x05
