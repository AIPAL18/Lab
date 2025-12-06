# Projet : Jeu-de-la-vie
# Auteurs : Elie RUGGIERO

from __future__ import annotations

from typing import TypeVar, NoReturn, Union, Generic, Iterable
from types import NoneType, GenericAlias
from abc import ABC
from copy import deepcopy
from singleton import Singleton


__all__ = [
    "make_shared",
    "OptPtr",
    "ptr",
    "shared_ptr",
]

# Python 3.12+ (PEP 695)
type OptPtr[T] = Union[T, None]  # in case nullptr is implemented


class FrozenMeta(type):
    __slots__ = ()
    
    def __new__(cls, name, bases, dct):
        # We need __frozen because otherwise, we're not able to add any attribute during the creation of the new class, then we freeze it.
        inst = super().__new__(cls, name, bases, {"_FrozenMeta__frozen": False, **dct})
        inst.__frozen = True
        return inst

    def __setattr__(self, key, value):
        if self.__frozen and not hasattr(self, key):
            raise TypeError("I am frozen")
        super().__setattr__(key, value)

class ptr(FrozenMeta):
    __slots__ = ()


class shared_ptr[T: type = object](metaclass=ptr):
    # __slots__ prevents the creation of __weakref__ for shared_ptr, this behaviour is desired
    __slots__ = ("__obj", "__orig_class__")
    private = ("get", "reset", "swap", "base", "unique", "use_count")
    count_dict: dict[object: int] = {}
    
    def __init__(self, obj: T):
        if obj in shared_ptr.count_dict:
            shared_ptr.count_dict[obj] += 1
        else:
            shared_ptr.count_dict[obj] = 1
        self.__obj = obj

    @classmethod
    def __class_getitem__(cls, key: T):
        # https://docs.python.org/3/reference/datamodel.html#object.__class_getitem__
        if not isinstance(key, Iterable):
            return GenericAlias(cls, key)
        else:
            raise TypeError("An object cannot be of several types at the same time")

    def __getattribute__(self, name):
        if not name:
            return
        elif name[0] == "_" or name in shared_ptr.private:
            return super().__getattribute__(name)
        elif self.__obj is None:
            return  # Don't know what to do
        return self.__obj.__getattribute__(name)
    
    def __setattr__(self, name, value):
        if name[0] == "_" or name in shared_ptr.private:
            return super().__setattr__(name, value)
        elif self.__obj is None:
            return  # Don't know what to do
        return self.__obj.__setattr__(name, value)
    
    def __bool__(self) -> bool:
        return self.__obj is not None

    def __call__(self, obj: object) -> NoReturn:
        if self.__obj:
            self.reset()
        self.__obj = obj
    
    def reset(self) -> NoReturn:
        if self.__obj is None:
            return
        
        shared_ptr.count_dict[self.__obj] -= 1
        if shared_ptr.count_dict[self.__obj] == 0:
            del shared_ptr.count_dict[self.__obj]
        self.__obj = None
    
    def get(self) -> T:
        return self.__obj
    
    def base(self) -> type:
        if hasattr(self, "__orig_class__"):
            base = self.__orig_class__.__args__[0]
            if isinstance(base, TypeVar):
                return base.__default__
            else:
                return base
        else:
            return NoneType

    def use_count(self) -> int:
        return shared_ptr.count_dict[self.__obj]
    
    def unique(self) -> bool:
        return self.use_count() == 1

    def swap(self, pointer: shared_ptr):
        if pointer.get() is self.__obj:
            return
        obj1 = pointer.get()
        pointer(self.__obj)
        self.__call__(obj1)


class make_shared[T: type = object](metaclass=FrozenMeta):
    __slots__ = ()
    
    def __new__(cls, obj: T) -> T:
        if isinstance(obj, type):
            raise TypeError("Cannot share a type")
        if isinstance(obj, shared_ptr):
            return shared_ptr[T](obj.get())

        return shared_ptr[T](obj)

    @classmethod
    def __class_getitem__(cls, key):
        # https://docs.python.org/3/reference/datamodel.html#object.__class_getitem__
        if not isinstance(key, Iterable):
            return GenericAlias(cls, key)
        else:
            raise TypeError("An object cannot be of several types at the same time")


if __name__ == "__main__":
    # https://www.geeksforgeeks.org/shared-reference-in-python/
    class Foo:
        def __init__(self, var):
            self.var = var 
        
        def set(self, ma_var) -> None:
            self.var = ma_var
    

    class Bar(Foo):
        def __init__(self, var):
            self.var = var 
        
        def set(self, ma_var) -> None:
            self.var = ma_var

    shared_foo = make_shared[Foo](Bar(100))
    shared_bar = make_shared(Bar(100))

    type eniter = list[int]
    
    print(shared_foo.base())
    print(shared_bar.base())
    