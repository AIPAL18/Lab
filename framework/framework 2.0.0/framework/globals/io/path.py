# Projet : Jeu-de-la-vie
# Auteurs : Elie RUGGIERO

from __future__ import annotations
from pathlib import Path
from os import sep as path_sep

__all__ = [
    "path",
]


def path(p: str) -> str:
    path_obj = Path(p)
    if not path_obj.exists():
        print("The following path doesn't exist: {p}")
        pass

    if path_obj.drive or path_obj.root:
            return path_obj.drive + path_obj.root + path_sep.join(path_obj._tail)
    
    return path_sep.join(path_obj._tail)


if __name__ == "__main__":
    print(path("C:/Users/elier/Documents/Code"))
