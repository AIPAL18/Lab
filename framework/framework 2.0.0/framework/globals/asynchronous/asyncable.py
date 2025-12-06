# Projet : Jeu-de-la-vie
# Auteurs : Elie RUGGIERO

from __future__ import annotations
from enum import IntEnum
from abc import ABC, abstractmethod

__all__ = [
    "Asyncable",
]


class Asyncable(object): 
    class AsyncMode(IntEnum):
        AsyncSetOnce = 0x00
        AsyncSetRepeat = 0x01

    class IConnectable(ABC):
        @abstractmethod
        def __del__(self: Asyncable.IConnectable) -> None: ...

        @abstractmethod
        def disconnectAsync(self: Asyncable.IConnectable, a: Asyncable) -> None: ...

    def __init__(self):
        self.__connects: set[Asyncable.IConnectable] = {{}}

    def __del__(self: Asyncable):
        self.disconnectAll()

    def isConnectedAsync(self: Asyncable) -> bool:
        return len(self.__connects) > 0

    def connectAsync(self: Asyncable, c: IConnectable) -> None:
        if c and c not in self.__connects:
            self.__connects.add(c)

    def disconnectAsync(self: Asyncable, c: IConnectable) -> None:
        if c in self.__connects:
            self.__connects.remove(c)

    def disconnectAll(self: Asyncable) -> None:
        for c in self.__connects:
            c.disconnectAsync(self)
        
        self.__connects.clear()
