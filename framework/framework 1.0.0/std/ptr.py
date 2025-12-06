from __future__ import annotations
from typing import (_SpecialForm, Any, ClassVar, Final, ForwardRef, Generic, 
                    Literal, LiteralString, Never, NoReturn, Protocol, Self, 
                    TypeAlias, TypeVar, Union)
from types import NoneType, GenericAlias
from abc import ABC

T = TypeVar("T")

__all__ = [
    "make_shared",
    "nullptr",
    "Optionalptr",
    "ptr",
    "shared_ptr",
]

class ptr(ABC, Generic[T]): ...


class nullptr(ptr):
    def __new__(cls):
        # Pattern Singleton
        if not hasattr(cls, "instance"):
            cls.instance = super().__new__(cls)

        return cls.instance
    
    def __bool__(self) -> Literal[False]:
        return False

    def __call__(self, *args, **kwds) -> nullptr:
        return self
    
    def __int__(self) -> int:
        return int()

    def __str__(self) -> str:
        return str()


class shared_ptr(ptr[T]):
    slots = ("get", "reset", "swap", "type", "unique", "use_count")
    count_dict: dict[object: int] = {}
    
    def __new__(cls, obj: Optionalptr[T] = None) -> shared_ptr[T]:
        if cls.type() is NoneType:
            cls.__type = type(obj)

        instance = super().__new__(cls)
        instance.__obj  = obj
    
        if obj in shared_ptr.count_dict:
            shared_ptr.count_dict[obj] += 1
        elif obj is None:
            pass
        else:
            shared_ptr.count_dict[obj] = 1

        return instance

    @classmethod
    def __class_getitem__(cls, key):
        # https://docs.python.org/3/reference/datamodel.html#object.__class_getitem__
        cls.__type = key
        return super().__class_getitem__(key)
    
    @classmethod
    def type(cls) -> type:
        # Private members: 
        # https://www.geeksforgeeks.org/private-attributes-in-a-python-class/
        if hasattr(cls, f"_{shared_ptr.__name__}__type"):
            return cls.__type
        return NoneType

    def __getattribute__(self, name):
        if name[0] == "_" or name in shared_ptr.slots:
            return super().__getattribute__(name)
        elif self.__obj is None:
            return
        return self.__obj.__getattribute__(name)
    
    def __setattr__(self, name, value):
        if name[0] == "_" or name in shared_ptr.slots:
            return super().__setattr__(name, value)
        elif self.__obj is None:
            return
        return self.__obj.__setattr__(name, value)
    
    def __bool__(self) -> bool:
        return self.__obj is not None

    def __del__(self):
        self.reset()

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
    
    def get(self) -> object:
        return self.__obj

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


class make_shared(Generic[T]):
    def __new__(cls, obj: T) -> shared_ptr[T]:
        if isinstance(obj, type):
            return
        if isinstance(obj, shared_ptr):
            obj = obj.get()

        return shared_ptr[type(obj)](obj)


def _type_convert(arg, module=None, *, allow_special_forms=False):
    """
    From typing

    For converting None to type(None), and strings to ForwardRef.
    """
    if arg is None:
        return NoneType
    if isinstance(arg, str):
        return ForwardRef(arg, module=module, is_class=allow_special_forms)
    return arg


def _type_check(arg, msg, is_argument=True, module=None, *, allow_special_forms=False):
    """
    From typing
    """
    invalid_generic_forms = (Generic, Protocol)
    if not allow_special_forms:
        invalid_generic_forms += (ClassVar,)
        if is_argument:
            invalid_generic_forms += (Final,)

    arg = _type_convert(arg, module=module, allow_special_forms=allow_special_forms)
    if (isinstance(arg, GenericAlias) and
            arg.__origin__ in invalid_generic_forms):
        raise TypeError(f"{arg} is not valid as type argument")
    if arg in (Any, LiteralString, NoReturn, Never, Self, TypeAlias):
        return arg
    if allow_special_forms and arg in (ClassVar, Final):
        return arg
    if isinstance(arg, _SpecialForm) or arg in (Generic, Protocol):
        raise TypeError(f"Plain {arg} is not valid as type argument")
    if type(arg) is tuple:
        raise TypeError(f"{msg} Got {arg!r:.100}.")
    return arg

@_SpecialForm
def Optionalptr(self, parameters):
    arg = _type_check(parameters, f"{self} requires a single type.")

    return Union[arg, NoneType, nullptr]


if __name__ == "__main__":
    class Foo(object):
        def __init__(self, var: Optionalptr[int] = None):
            self.var = var 
        
        def set(self, ma_var: Optionalptr[int] = None) -> None:
            self.var = ma_var
    
    shared_foo = shared_ptr[Foo](Foo(100))
    print(shared_foo.type())
    if not nullptr():
        print("Nullptr")
