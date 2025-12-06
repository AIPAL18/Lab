# Projet : Jeu-de-la-vie
# Auteurs : Elie RUGGIERO

from __future__ import annotations
from typing import TypeVar, Generic
from ..internal.multipledispatch import dispatch

T = TypeVar("T")

__all__  = [
    
]


class Channel(Generic[T]):
    @dispatch()
    def __init__(self: Channel):
        super().__init__()

    @dispatch()
    def __init__(self: Channel, ch: Channel):
        super().__init__()
        self.__ptr = ch.ptr()
    
    def set(self: Channel, ch: Channel):
        self.__ptr = ch.ptr()
