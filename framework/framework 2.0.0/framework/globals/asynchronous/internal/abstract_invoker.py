# Projet : Jeu-de-la-vie
# Auteurs : Elie RUGGIERO

from __future__ import annotations
from threading import Lock, get_ident
from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Any, Callable
from framework.globals import std
from ..asyncable import Asyncable
from copy import deepcopy
from multipledispatch import dispatch
from queued_invoker import QueuedInvoker

T = TypeVar("T")

__all__ = [
    "NotifyData",
    "AbstractInvoker",
]


class NotifyData(object):
    class Arg(Generic[T]):
        def __init__(self: NotifyData.Arg, *values: T) -> None:
            super().__init__()
            self.val: tuple[T] = values

    def __init__(self: NotifyData) -> None:
        super().__init__()
        self.__args: list[std.shared_ptr[T]] = []
    
    def setArg(self: NotifyData, i: int, *values: T) -> None:
        p = self.Arg[T](*values)
        self.__args.insert(i, std.make_shared(p))
    
    def arg(self: NotifyData, i: int = 0) -> Any:
        p: NotifyData.Arg = self.__args[i].get()
        if not p:
            return None

        return p.val[0]

    def args(self: NotifyData, i: int = 0) -> tuple[Any]:
        p: NotifyData.Arg = self.__args[i].get()
        if not p:
            return None

        return p.val


class AbstractInvoker(Asyncable.IConnectable):
    """
    void disconnectAsync(Asyncable* receiver);

    void invoke(int type);
    void invoke(int type, const NotifyData& data);

    bool isConnected() const;

    static void processEvents();
    static void onMainThreadInvoke(const std::function<void(const std::function<void()>&, bool)>& f);
    """
    def disconnectAsync(self: AbstractInvoker, receiver: Asyncable) -> None:
        types: list[int] = []
        for it in self._callbacks.values():
            for c in it:
                c: AbstractInvoker.CallBack
                if c.receiver == receiver:
                    types.append(c.type)

        for t in types:
            self._removeCallBack(t, receiver)

    @dispatch(int)
    def invoke(self: AbstractInvoker, type: int) -> None:
        self.invoke(type, NotifyData())

    @dispatch(int, NotifyData)
    def invoke(self: AbstractInvoker, type: int, data: NotifyData) -> None:
        it: AbstractInvoker.CallBacks = self._callbacks.get(type, None)
        if it is None:
            return

        threadID = get_ident()
        
        # NOTE: explicit copy because collection can be modified from elsewhere
        callbacks: AbstractInvoker.CallBacks = deepcopy(it)

        for c in callbacks:
            c: AbstractInvoker.CallBack
            if not it.contains_receiver(c.receiver):
                print("Skipping removed receiver")
                continue
            if c.threadID == threadID:
                self._invokeCallback(type, c, data)
            else:
                qi = AbstractInvoker.QInvoker(self, type, c, data)
                QueuedInvoker.instance().invoke(c.threadID, lambda: self.__invoke_qi(qi))
    
    def __invoke_qi(self: AbstractInvoker, qi: AbstractInvoker.QInvoker) -> None:
        qi.invoke()
        del qi

    def isConnected(self: AbstractInvoker) -> bool:
        for cs in self._callbacks:
            cs: AbstractInvoker.CallBacks
            if len(cs) > 0:
                return True
        
        return False

    def processEvents(self: AbstractInvoker) -> None:
        QueuedInvoker.instance().processEvents()

    def onMainThreadInvoke(self: AbstractInvoker, f: Callable[[Callable[[], None], bool], None]) -> None:
        QueuedInvoker.instance().onMainThreadInvoke(f)

# protected

    def __init__(self):
        super().__init__()
        self._callbacks: dict[int: AbstractInvoker.CallBacks] = {}
        self._qInvokersMutex = Lock()
        self._qInvokers = list[AbstractInvoker.QInvoker] = []
    
    def __del__(self):
        with self._qInvokersMutex:
            for qi in self._qInvokers:
                qi: AbstractInvoker.QInvoker
                qi.invalidate()
    
    
    #! TODO: change the type of `call` (void ptr in c++)
    
    @abstractmethod
    def _deleteCall(self: AbstractInvoker, type: int, call: Any) -> None: ...

    @abstractmethod
    def _doInvoke(self: AbstractInvoker, type: int, call: Any, data: NotifyData) -> None: ...

    class CallBack(object):
        """
        std::thread::id threadID;
        int type = 0;
        Asyncable* receiver = nullptr;
        void* call = nullptr;
        CallBack() = default;
        CallBack(std::thread::id threadID, int t, Asyncable* cr, void* c)
            : threadID(threadID), type(t), receiver(cr), call(c) {}
        """
        threadID: int = 0
        type: int = 0
        receiver: Asyncable = std.nullptr()
        call: Any = std.nullptr()
        
        @dispatch()
        def __init__(self):
            super().__init__()
        
        @dispatch()
        def __init__(self, threadID: int, t: int, cr: Asyncable, c: Any):
            super().__init__()
            self.threadID = threadID
            self.type = t
            self.receiver = cr
            self.call = c
    
    class CallBacks(list[CallBack]):
        def receiverIndexOf(self, receiver: Asyncable) -> int:
            for i in range(len(self)):
                if self[i].receiver == receiver:
                    return i
            
            return -1

        def containsReceiver(self, receiver: Asyncable) -> bool:
            return self.receiverIndexOf(receiver) > -1
    
    class QInvoker(object):
        mutex = Lock()
        invoker: AbstractInvoker = std.nullptr()
        type: int = -1
        call: AbstractInvoker.CallBack
        data: NotifyData
        
        def __init__(self: AbstractInvoker.QInvoker,  i: AbstractInvoker,  t: int,  c: AbstractInvoker.CallBack,  d: NotifyData) -> None:
            self.invoker = i
            self.type = t
            self.call = c
            self.data = d

            self.invoker._addQInvoker(self)
        
        def __del__(self: AbstractInvoker.QInvoker) -> None:
            if self.invoker:
                self.invoker._removeQInvoker(self)
    
        def invoke(self: AbstractInvoker.QInvoker) -> None:
            inv: AbstractInvoker = std.nullptr()
            with self.mutex:
                inv = self.invoker
            
            if inv:
                inv._invokeCallback(self.type, self.call, self.data)
        
        def invalidate(self: AbstractInvoker.QInvoker) -> None:
            with self.mutex:
                invoker = std.nullptr()

    def _invokeCallback(self: AbstractInvoker, type: int, c: CallBack, data: NotifyData):
        assert c.threadID == get_ident()

        if not self._containsReceiver(c.receiver):
            return

        if c.receiver and not c.receiver.isConnectedAsync():
            return
        
        self._doInvoke(type, c.call, data)
    
    def _addCallBack(self: AbstractInvoker, type: int, receiver: Asyncable, call: Any, mode: Asyncable.AsyncMode = Asyncable.AsyncMode.AsyncSetRepeat) -> None:
        callbacks: AbstractInvoker.CallBacks = self._callbacks[type]
        if callbacks.containsReceiver(receiver):
            match mode:
                case Asyncable.AsyncMode.AsyncSetOnce:
                    self._deleteCall(type, call)
                    return
                case Asyncable.AsyncMode.AsyncSetRepeat:
                    self._removeCallBack(type, receiver)
        
        c = AbstractInvoker.CallBack(get_ident(), type, receiver, call)
        self._callbacks[type].append(c)
        if c.receiver:
            c.receiver.connectAsync(self)

    def _removeCallBack(self: AbstractInvoker, type: int, receiver: Asyncable) -> None:
        it = self._callbacks.get(type)
        if it is None:
            return
    
        callbacks: AbstractInvoker.CallBacks = deepcopy(it)
        index: int = callbacks.receiverIndexOf(receiver)
        if index < 0:
            return

        c: AbstractInvoker.CallBack = callbacks[index]
        if c.receiver:
            c.receiver.disconnectAsync(self)

        callbacks.pop(index)

        with self._qInvokersMutex:
            for qi in self._qInvokers:
                qi: AbstractInvoker.QInvoker
                if qi.call.call == c.call:
                    qi.invalidate()
                    break
        
        self._deleteCall(type, c.call)

    def _removeAllCallBacks(self: AbstractInvoker) -> None:
        for it in self._callbacks.values():
            for c in it:
                c: AbstractInvoker.CallBack
                if c.receiver:
                    c.receiver.disconnectAsync(self)
                self._deleteCall(c.type, c.call)
        
        self._callbacks.clear()
        

    def _addQInvoker(self: AbstractInvoker, qi: QInvoker) -> None:
        with self._qInvokersMutex:
            self._qInvokers.append(qi)

    def _removeQInvoker(self: AbstractInvoker, qi: QInvoker) -> None:
        with self._qInvokersMutex:
            self._qInvokers.remove(qi)

    def _containsReceiver(self: AbstractInvoker, receiver: Asyncable) -> bool:
        for it in self._callbacks.values():
            for c in it:
                c: AbstractInvoker.CallBack
                if c.receiver == receiver:
                    return True
        
        return False
