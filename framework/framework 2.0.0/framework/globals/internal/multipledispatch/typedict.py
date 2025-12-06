# Projet : Jeu-de-la-vie
# Auteurs : Elie RUGGIERO

from __future__ import annotations
from typing import Callable, Generic, TypeVar, Any

T = TypeVar("T")
# Instance unique d'un objet pour représenter un objet vide, car None est une
# valeur qui peut être significative
null = object()

__all__ = [
    "TypeDict",
    "Optional",
]


class Optional(Generic[T]):
    def __init__(self):
        super().__init__()
        self.valeur = null
    
    def empty(self) -> bool:
        return self.valeur is null
    
    def set(self, valeur: T) -> None:
        self.valeur = valeur
    
    def get(self, defaut: T | None = None) -> T:
        return self.valeur if not self.empty() else defaut


class TypeDict(dict[tuple[type, ...]: Callable]):
    def __contains__(self, key: tuple):
        # if super().__contains__(key):
        #     return True
        
        # i = 0
        # trouve = False
        # it = self.__iter__()
        # while i < len(self) and not trouve:
        #     element: tuple[type, ...] = next(it)
        #     print(element)
        #     if len(key) == len(element):
        #         valide = True
        #         j = 0
        #         while j < len(element) and valide:
        #             if not isinstance(key[j], element[j]):
        #                 valide = False
        #                 trouve = True
        #             j += 1
        #     i += 1
        
        # return trouve
        return super().__contains__(key)
    
    def get_optional(self, key: tuple[object, ...]) -> Optional:
        func = Optional()
        if super().__contains__(key):
            func.set(self[key])
            return func
        
        i = 0
        trouve = False
        it = self.__iter__()
        while i < len(self) and not trouve:
            element: tuple[type, ...] = next(it)
            print(element)
            if len(key) == len(element):
                valide = True
                j = 0
                while j < len(element) and valide:
                    if not isinstance(key[j], element[j]):
                        valide = False
                        trouve = True
                        func.set(self[element])
                    j += 1
            i += 1
        
        return func
