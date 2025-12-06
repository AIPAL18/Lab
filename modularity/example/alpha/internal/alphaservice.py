from ..ialphaservice import IAlphaService
from typing import override


class AlphaService(IAlphaService):
    @override
    def info(self) -> str:
        return "alpha"
