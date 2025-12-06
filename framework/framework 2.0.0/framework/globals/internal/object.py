# Projet : Jeu-de-la-vie
# Auteurs : Elie RUGGIERO

from __future__ import annotations
from shiboken6 import Shiboken
from copy import deepcopy
from typing import TypeVar
T = TypeVar("T")

__all__ = [
    "BaseObject",
    "Object",
]


class BaseObject(object):
    """
    Define an object and gives it handlers.

    Inheritance:
        Shiboken.Object
    """
    __obj__ = True
    
    def __init_subclass__(cls: type):
        print("Init sub", cls.__base__)

        cls.__obj__ = True
        new = deepcopy(cls.__new__)
        init = deepcopy(cls.__init__)

        def __new__(_cls, *args, **kwds):
            return new(_cls, *args, **kwds)
        
        def __call__(self, *args, **kwds) -> None:
            init(self, *args, **kwds)
        
        cls.__new__ = __new__
        cls.__call__ = __call__


class Object:
    """
    A class decorator to avoid problems (often `TypeError`)
    """
    __obj__ = False

    def __new__(cls: type, other: type[T]) -> T:
        """
        https://www.stemkb.com/python/the-__bases__-attribute-in-python.htm
        https://stackoverflow.com/a/9541560/15793884
        """
        bases =  other.__mro__[:-1] + (BaseObject,) + (other.__mro__[-1],)
        new = type(other.__name__, bases, dict(other.__dict__))
        return new
