# Projet : Jeu-de-la-vie
# Auteurs : Elie RUGGIERO

from __future__ import annotations
from enum import IntEnum
from multipledispatch import dispatch
from typing import Any

__all__ = [
    
]


class Ret(object):
    class Code(IntEnum):
        Undefined       = -1
        Ok              = 0
        UnknownError    = 1

        # not error, just codes
        Cancel          = 3  # abort by user

        NotSupported    = 4
        NotImplemented  = 5

        # Global errors
        GlobalFirst     = 20
        InternalError   = 21
        GlobalLast      = 99

        UiFirst         = 100
        UiLast          = 199

        ExtensionsFirst = 200
        ExtensionsLast  = 299

        AudioFirst      = 300
        AudioLast       = 399

        SystemFirst     = 400
        SystemLast      = 499

        NetworkFirst    = 500
        NetworkLast     = 599

        MidiFirst       = 600
        MidiLast        = 699

        LanguagesFirst  = 700
        LanguagesLast   = 799

        NotationFirst   = 1000
        NotationLast    = 1299

        ConverterFirst  = 1300
        ConverterLast   = 1399

        VstFirst        = 1400
        VstLast         = 1499

        WorkspaceFirst  = 1500
        WorkspaceLast   = 1599

        LearnFirst      = 1600
        LearnLast       = 1699

        UpdateFirst  = 1700
        UpdateLast   = 1799

        CloudFirst   = 1800
        CloudLast    = 1899

        EngravingFirst  = 2000
        EngravingLast   = 2999

        ProjectFirst  = 3000
        ProjectLast   = 3999

        DiagnosticsFirst = 4000
        DiagnosticsLast = 4999

    @dispatch()
    def __init__(self: Ret) -> None:
        super().__init__()
        self.__code = self.Code.Undefined.value
        self.__text = str()
        self.__data: dict[str: Any] = {}
    
    @dispatch(bool)
    def __init__(self: Ret, arg: bool) -> None:
        self.__init__()
        self.__code = self.Code.Ok.value if arg else self.Code.UnknownError.value
    
    @dispatch(int)
    def __init__(self: Ret, c: int) -> None:
        self.__init__()
        self.__code = c
    
    @dispatch(Code)
    def __init__(self: Ret, c: Code) -> None:
        self.__init__()
        self.__code = c.value
    
    @dispatch(int, str)
    def __init__(self: Ret, c: int, text: str) -> None:
        self.__init__()
        self.__code = c
        self.__text = text

    def setCode(self: Ret, c: int):
        self.__code = c

    def code(self: Ret) -> int:
        return self.__code
    
    def valid(self: Ret) -> bool:
        return self.__code > self.Code.Undefined.value
    
    def success(self: Ret) -> bool:
        return self.__code == self.Code.Ok.value
    
    def setText(self: Ret, s: str) -> None:
        self.__text = s
    
    def text(self: Ret) -> str:
        return self.__text
    
    def setData(self: Ret, key: str, val: Any) -> None:
        self.__data[key] = val
    
    def data(self: Ret, key: str) -> Any:
        return self.__data.get(key, None)
    
    def __bool__(self: Ret) -> bool:
        return self.success()
    
    def __str__(self: Ret) -> str:
        return f"[{self.__code}] {self.__text}"
    
    def __eq__(self, other: Ret) -> bool:
        return self.__code == other.__code and self.__text == other.__text and self.__data == other.__data


def make_ok() -> Ret:
    return Ret(Ret.Code.Ok)

def check_ret(r: Ret, c: Ret.Code) -> bool:
    return r.code() == c.value
