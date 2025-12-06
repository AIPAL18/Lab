from __future__ import annotations
from ..interfaces import IAlphaService
from typing import override


class AlphaService(IAlphaService):
    def __init__(self: AlphaService) -> None:
        super().__init__()
    
    @override
    def info(self: AlphaService) -> str:
        return "alpha"
