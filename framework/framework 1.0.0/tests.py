from __future__ import annotations
from types import *
from typing import *

AnyStr = TypeVar('AnyStr', str, bytes)


def concat(x: AnyStr, y: AnyStr) -> AnyStr:
    return x + y


def testinfo[I: Any](coucou: I):
    return type(I)


print(concat("coucou", "coucou"))
print(testinfo("coucou"))