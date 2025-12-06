# Projet : Jeu-de-la-vie
# Auteurs : Elie RUGGIERO

from __future__ import annotations
from functools import partial
from typing import TypeVar

T = TypeVar("T")


class Singleton(object):
    def __new__(main_cls, singleton_cls: T) -> T:
        ctor = partial(singleton_cls.__new__, singleton_cls)
        
        def __new__(cls: T, *args, **kwds):
            if not hasattr(cls, f"_{cls.__name__}__instance"):
                # cls.__instance = ctor(*args, **kwds)
                cls.__instance = super(singleton_cls).__new__(*args, **kwds)
            
            return cls.__instance

        @classmethod
        def instance(cls: T) -> T:
            if not hasattr(cls, f"_{cls.__name__}__instance"):
                return cls.__new__()
            
            return cls.__instance

        singleton_cls.__new__ = __new__
        # setattr(singleton_cls, "instance", instance)

        return singleton_cls
    

if __name__ == "__main__":
    @Singleton
    class Test(object):
        # def __new__(cls, var):
        #     print("Test")
        #     return super().__new__(cls)

        def __init__(self, var):
            self.var = var
        
        def __repr__(self):
            return str(self.var)
    

    class Test2(object):
        def __new__(cls, *args, **kwds):
            if not hasattr(cls, f"_{cls.__name__}__instance"):
                cls.__instance = super().__new__(cls)
            
            return cls.__instance

        def __init__(self, var):
            self.var = var
        
        def __repr__(self):
            return str(self.var)

    t = Test2(1)
    t2 = Test2(2)
    print(t is t2)
