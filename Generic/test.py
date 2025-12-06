from functools import partial, wraps
from typing import Callable, TypeVar, Iterable, Any, ParamSpec

T = TypeVar('T', bound=type)
R = TypeVar('R')
P = ParamSpec('P')

class Meta(type):
    def __get__(self, instance, owner=None):
        print(instance, owner)
        return self


def template(name: str = "", /, *, default: Any = None) -> Callable[[Callable[P, R]], Callable[..., Any]]:
    
    def helper(fun: Callable[P, R]) -> Callable[..., Any]:

        class Inner(metaclass=Meta):
            @wraps(fun)
            def __new__(cls, *args: P.args, **kwargs: P.kwargs):
                return fun(*args, **{name: default, **kwargs})

        return Inner
    
    return helper


if __name__ == "__main__":
    class A:
        def __init__(self, var):
            self.var = var
        
        @template("T")
        def check(T: type) -> bool:
            return T
    
    a = A(1)
    print(a.check())