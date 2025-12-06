"""
# bind

Bind a object with its interface
"""

__version__ = "1.0.0"

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

from .bind import (
    isinterface, is_bound, set_bound, Bound, bind, BoundProxyInterface, 
    BoundProxy, proxy
)
