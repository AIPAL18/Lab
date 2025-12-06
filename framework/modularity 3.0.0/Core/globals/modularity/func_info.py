# Projet : Jeu-de-la-vie
# Auteurs : Elie RUGGIERO

from __future__ import annotations
import inspect
from typing import Any

__all__ = [
    "classFunc",
    "className",
    "funcSig",
    "funcName",
    "moduleName",
]


def get_param_types(parameters: dict[str, inspect.Parameter]) -> list[str]:
    types = []
    for value in parameters.values():
        value: inspect.Parameter
        if value is inspect._empty:
            print("Descriptor's parameters must be annotated!")
            types.append(Any)
        else:
            types.append(value.annotation.__name__)
        
    return types


def get_return_type(sig: inspect.Signature):
    if sig.return_annotation is inspect._empty:
        print("Descriptor must be annotated!")
        # Par sécurité, on retourne Any
        return Any 
    
    return sig.return_annotation.__name__


def funcName(obj: object) -> str:
    """
    Une fonction qui ne retourne rien être annotée "NoReturn" et retourner "NoReturn"
    """
    if inspect.isfunction(obj) or inspect.ismethod(obj):
        return obj.__name__
    
    return ""


def className(obj: object) -> str:
    """
    Une fonction qui ne retourne rien être annotée "NoReturn" et retourner "NoReturn"
    """
    sep = "."
    if inspect.isfunction(obj) or inspect.ismethod(obj):
        qualname: str = obj.__qualname__
        if sep in qualname:
            # TODO: Décider:
            """
            Pour une classe de la forme
            class FOO:
                class Foo:
                    def foo(a: int, b: type, c: Union[int, tuple], d: T, e: Optional[bool] = None) -> NoReturn:
                        return NoReturn
            
            Que doit-on retourner ?
            La classe direct ? (qualname.rpartition(sep)[0].rpartition(sep)[2])
                Foo
            La branche jusqu'à la classe mère ? (qualname.rpartition(sep)[0])
                FOO.Foo
            """
            return qualname.rpartition(sep)[0]
            # return qualname.rpartition(sep)[0].rpartition(sep)[2]
    
    return ""
    

def classFunc(obj: object | type) -> str:
    # Duck typing
    # if inspect.isfunction(obj) or inspect.ismethod(obj):
    if hasattr(obj, "__qualname__"):
        return obj.__qualname__
    
    return ""


def moduleName(obj: object | type) -> str:
    # Duck typing
    # if inspect.isfunction(obj) or inspect.ismethod(obj):
    if hasattr(obj, "__module__"):
        if obj.__module__ != "__main__":
            return obj.__module__
    
    return ""


def funcSig(obj: object) -> str:
    """
    Une fonction qui ne retourne rien être annotée "NoReturn" et retourner "NoReturn"
    """
    if inspect.isfunction(obj) or inspect.ismethod(obj):
        signature: inspect.Signature = inspect.signature(obj, eval_str=True)
        
        param = signature.parameters.copy()
        if param.get('self', False):
            del param['self']
        
        args_type = get_param_types(param)
        return_type = get_return_type(signature)
        module = moduleName(obj)
        qualname = obj.__qualname__
        
        return f"{module} {qualname}({", ".join(args_type)}) -> {return_type}"
    
    return ""
