# Projet : Jeu-de-la-vie
# Auteurs : Elie RUGGIERO

from __future__ import annotations
from typing import TypeVar

try:
    from .object import BaseObject
except ImportError:
    class BaseObject: 
        __module__ = "object"
        __name__ = "BaseObject"

__all__ = [
    "new",
]

T = TypeVar("T")


def new(obj: type[T]) -> T:
    # https://www.geeksforgeeks.org/duck-typing-in-python/
    if hasattr(obj, "__obj__"):
        return obj.__new__(obj)
    
    raise NotImplementedError(f"new function is only implemented for {BaseObject.__module__}.{BaseObject.__qualname__} instances!")
