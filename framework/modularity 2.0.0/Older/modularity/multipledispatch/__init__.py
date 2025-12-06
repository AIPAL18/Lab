# Projet : Jeu-de-la-vie
# Auteurs : Elie RUGGIERO

r"""
# multipledispatch

Cette librairie dérivée du module multipledispatch 
(https://pypi.org/project/multipledispatch/), disponible sur le dépots 
GitHub suivant:
https://github.com/mrocklin/multipledispatch/tree/main/multipledispatch
"""

from .core import dispatch
from .dispatcher import (
    Dispatcher,
    halt_ordering,
    restart_ordering,
    MDNotImplementedError,
)

__version__ = "0.6.0"
