# Projet : Jeu-de-la-vie
# Auteurs : Elie RUGGIERO

from __future__ import annotations
from ...internal import Singleton
from ..asyncable import Asyncable
from typing import TypeVar, Generic
from abc import ABC, abstractmethod
from multipledispatch import dispatch
from threading import Lock, get_ident
from .queued_invoker import QueuedInvoker

F = TypeVar("F")
Arg1 = TypeVar("Arg1")

__all__ = [
    "AsyncImpl",
]


class AsyncImpl(Asyncable.IConnectable):
    class IFunction(ABC):
        def __del__(self) -> None:
            super().__del__()
            
        @abstractmethod
        def call(self) -> None: ...
    
    class Function(IFunction, Generic[F]):
        functor: F
        def __init__(self, fn: F) -> None:
            super().__init__()
            self.functor = fn
        
        def call(self) -> None:
            self.functor()
    
    class FunctionArg1(IFunction, Generic[F, Arg1]):
        functor: F
        arg1: Arg1
        def __init__(self, fn: F, a1: Arg1) -> None:
            super().__init__()
            self.functor = fn
            self.arg1 = a1
        
        def call(self) -> None:
            self.functor(self.arg1)
    
    class Call(object):
        caller: Asyncable = None
        func: AsyncImpl.IFunction = None
        
        @dispatch()
        def __init__(self) -> None:
            super().__init__()
        
        @dispatch(Asyncable, object)  #! NOTE: replace with AsyncImpl.IFonction
        def __init__(self, c: Asyncable, f: AsyncImpl.IFunction) -> None:
            self.caller = c
            self.func = f

    def __new__(cls, *args, **kwds) -> AsyncImpl:
        if not hasattr(cls, f"_{cls.__name__}__instance"):
            cls.__instance = super().__new__(cls)
        
        return cls.__instance
    
    def __init__(self) -> None:
        super().__init__()
        self.__mutex = Lock()
        self.__calls: dict[int, AsyncImpl.Call] = {}
    
    def call(self, caller: Asyncable, f: IFunction, th_id: int = get_ident()) -> None:
        if caller:
            caller.connectAsync(self)
        
        key = id(f)
        with self.__mutex:
            self.__calls[key] = caller
        
        functor = lambda: self.__onCall(key)
        QueuedInvoker.instance().invoke(th_id, functor, True)
    
    def disconnectAsync(self, caller: Asyncable) -> None:
        with self.__mutex:
            key = 0
            for k, value in self.__calls.items():
                if value is caller:  # == ?
                    key = k
            if key:
                self.__calls.pop(key)

    def __onCall(self: AsyncImpl, key: int) -> None:
        c = AsyncImpl.Call()
        with self.__mutex:
            if key in self.__calls:
                c = self.__calls.pop(key)
        
        c.func.call()

        if c.caller:
            c.caller.disconnectAsync(self)
        
        del c.func
