from abc import ABC, abstractmethod
import types

type Any = object
type void = None

__all__ = [
    "isinterface",
    "is_bound",
    "set_bound",
    "Bound",
    "bind",
    "BoundProxyInterface",
    "BoundProxy",
    "proxy",
]


def isinterface(obj, interface) -> bool:
    if not isinstance(interface, type):
        return False
    if not isinstance(obj, interface):
        return False
    
    return True


def is_bound(obj) -> bool:
    return getattr(obj, "__bound__", False)


def set_bound(obj: object):
    setattr(obj, "__bound__", True)


class Bound[T]:
    __bound__ = True
    
    def __init__(self, obj: T, interface: type) -> void:
        self.__wrapped_obj = obj
        self.__interface = interface

    def base(self) -> type:
        return self.__interface

    def __call__(self) -> T:
        return self.__wrapped_obj


def bind[T](obj: T, interface: type) -> Bound[T]:
    if not isinterface(obj, interface):
        raise TypeError(f"{interface!r} isn't an interface for {obj!r}.")
    
    assert not hasattr(obj, "__bound__"), "Not good, need to check properly"
    
    return Bound(obj, interface)


class BoundProxyInterface(ABC):
    """
    Proxy's interface.
    """
    @abstractmethod
    def base(self) -> type: ...


type BoundProxy[T] = T | BoundProxyInterface


def proxy[T](obj: T, interface) -> BoundProxy[T]:
    if not isinterface(obj, interface):
        raise TypeError(f"{interface!r} isn't an interface for {obj!r}.")
    
    assert not hasattr(obj, "__bound__"), "Not good, need to check properly"
    
    def base(self):
        return interface
    
    setattr(obj, "base", types.MethodType(base, obj))
    set_bound(obj)
    return obj


if __name__ == "__main__":
    class InterfaceDeMonObjet:
        def ma_methode(self):
            raise NotImplementedError

    class MonObjet(InterfaceDeMonObjet):
        def ma_methode(self):
            return "Méthode appelée depuis MonObjet"
        
        def __repr__(self):
            return f"<MonObjet> xxx"
        
        def __eq__(self, value):
            print("MonObjet", value)
            return super().__eq__(value)
        

    # Création de l'objet
    obj = MonObjet()

    print(obj.ma_methode())  # Affiche "Méthode appelée depuis MonObjet"
    print(obj)  # Teste de __repr__()

    # bind

    bound = bind(obj, InterfaceDeMonObjet)
    print(bound.base())  # Affiche "InterfaceDeMonObjet"
    print(bound().ma_methode())  # Affiche "Méthode appelée depuis MonObjet"
    print(bound())  # Teste de __repr__()

    # proxy
    
    proxybind = proxy(obj, InterfaceDeMonObjet)
    print(proxybind.base())  # Affiche "InterfaceDeMonObjet"
    print(proxybind.ma_methode())  # Affiche "Méthode appelée depuis MonObjet"
    print(proxybind)  # Teste de __repr__()
