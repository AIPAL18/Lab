# Projet : Jeu-de-la-vie
# Auteurs : Elie RUGGIERO

"""
# internal
"""

# Please keep __all__ alphabetized within each category.
__all__ = [
    # instantiation
    "new",
    
    # object
    "BaseObject",
    "Object",

    # singleton
    "Singleton",
]


from .instantiation import (new)
from .object import (BaseObject, Object)
from .singleton import (Singleton)
