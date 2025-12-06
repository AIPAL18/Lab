# Projet : Jeu-de-la-vie
# Auteurs : Elie RUGGIERO

from __future__ import annotations
from typing import Callable
from collections import deque
from threading import RLock, get_ident
from collections import defaultdict

__all__ = [
    "QueuedInvoker",
]


class QueuedInvoker(object):
    def __new__(cls, *args, **kwds):
        if not hasattr(cls, f"_{cls.__name__}__instance"):
            cls.__instance = super().__new__(cls)
        
        return cls.__instance

    # @classmethod
    # def instance(cls: QueuedInvoker) -> QueuedInvoker:
    #     return cls.__new__()

    Fonctor = Callable[[], None]
    Queue = deque[Fonctor]

    def invoke(self, callbackTh_id: int, f: Fonctor, isAlwaysQueued: bool = False) -> None:
        if self.__onMainThreadInvoke:
            if callbackTh_id == self.__mainThreadID:
                self.__onMainThreadInvoke(f, isAlwaysQueued)
        
        with self.__mutex:
            self.__queues[callbackTh_id].append(f)
    
    def processEvents(self) -> None:
        q = QueuedInvoker.Queue()
        with self.__mutex:
            n: QueuedInvoker.Queue = self.__queues[get_ident()]
            if n is not None:
                q = n
        
        while len(q) > 0:
            f = q.pop()
            if f:
                f()
    
    def onMainThreadInvoke(self, f: Callable[[Fonctor, bool], None]) -> None:
        self.__onMainThreadInvoke = f
        self.__mainThreadID = get_ident()
    
    def __init__(self):
        super().__init__()
        self.__mutex = RLock()
        self.__queues: defaultdict[int: QueuedInvoker.Queue] = defaultdict(QueuedInvoker.Queue)
        self.__queues.setdefault()
        self.__onMainThreadInvoke: Callable[[QueuedInvoker.Fonctor, bool], None] = None
        self.__mainThreadID: int = None


if __name__ == "__main__":
    q = QueuedInvoker.Queue()
    queues: defaultdict[int: QueuedInvoker.Queue] = defaultdict(QueuedInvoker.Queue)
    
    print(queues)
    n: QueuedInvoker.Queue = queues[get_ident()]
    print(n)
    print(queues)