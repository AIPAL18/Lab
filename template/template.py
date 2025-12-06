from typing import Callable, Iterable, Self
from types import NoneType
from functools import partial, wraps

__all__ = [
    "template",
    "templatemethode",
]

type Any = object


class Meta(type):
    instance: Self
    def __get__(self, instance, owner=None):
        self.instance = instance
        return self


def templatemethode(name: str = "", /, *, default: type = NoneType) -> Callable:
    """
    
    """
    def helper[R, **P](fun: Callable[P, R]) -> Callable[P, R]:
        """
        The actual decorator, return a subscriptable callable
        """
        class Inner[T: type](metaclass=Meta):
            @classmethod
            @wraps(fun)
            def __class_getitem__(cls, item: T):
                """
                Inner[int]
                <=>
                partial(fun, int)
                """
                if not isinstance(item, Iterable):
                    if name:
                        return partial(fun, cls.instance, **{name: item})
                    else:
                        return partial(fun, cls.instance, item)
                else:
                    raise TypeError("An object cannot be of several types at the same time")
            
            @wraps(fun)
            def __new__(cls, *args: P.args, **kwargs: P.kwargs) -> R:
                """
                Inner()
                <=>
                fun()
                """
                if name:
                    return fun(cls.instance, *args, **{name: default, **kwargs})
                else:
                    return fun(cls.instance, default, *args, **kwargs)
        
        return Inner
        
    return helper


def template(name: str = "", /, *, default: type = NoneType) -> Callable:
    """
    
    """
    def helper[R, **P](fun: Callable[P, R]) -> Callable[P, R]:
        """
        The actual decorator, return a subscriptable callable
        """
        class Inner[T: type]:
            @classmethod
            @wraps(fun)
            def __class_getitem__(cls, item: T):
                """
                Inner[int]
                <=>
                partial(fun, int)
                """
                if not isinstance(item, Iterable):
                    if name:
                        return partial(fun, **{name: item})
                    else:
                        return partial(fun, item)
                else:
                    raise TypeError("An object cannot be of several types at the same time")
            
            @wraps(fun)
            def __new__(cls, *args: P.args, **kwargs: P.kwargs) -> R:
                """
                Inner()
                <=>
                fun()
                """
                if name:
                    return fun(*args, **{name: default, **kwargs})
                else:
                    return fun(default, *args, **kwargs)
        
        return Inner
        
    return helper
    

if __name__ == "__main__":
    class A:
        def __init__(self, var):
            self.var = var
        
        @templatemethode("T")
        def check(self, T: type) -> bool:
            return isinstance(self.var, T)
    
    a = A(1)
    print(a.check[int]())
    
    @template()
    def get(T: type, coucou: str):
        print(coucou)
        return T

    print(get[int]("bonjour"))
