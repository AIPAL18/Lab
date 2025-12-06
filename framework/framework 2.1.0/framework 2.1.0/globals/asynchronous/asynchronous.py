# Projet : Jeu-de-la-vie
# Auteurs : Elie RUGGIERO

from __future__ import annotations
from typing import Callable, Optional, Any
from threading import get_ident
from multipledispatch import dispatch
from .asyncable import Asyncable
from .internal.asynchronous_impl import AsyncImpl

__all__ = [
    "Async",
]


class Async(object):
    @staticmethod
    @dispatch(Asyncable, Callable, Optional[int])
    def call(caller: Asyncable, f: Callable, th_id: int = get_ident()) -> None:
        AsyncImpl().call(caller, AsyncImpl.Function(f), th_id)
    
    @staticmethod
    def call(caller: Asyncable, a1: Any, f: Callable, th_id: int = get_ident()) -> None:
        AsyncImpl().call(caller, AsyncImpl.FunctionArg1(f, a1), th_id)
    
    @staticmethod
    def disconnectAsync(a: Asyncable) -> None:
        AsyncImpl().disconnectAsync(a)
