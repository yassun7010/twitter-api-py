from .operator import Operator


class Keyword(Operator):
    def __init__(self, keyword: str) -> None:
        self._keyword = keyword

    def __str__(self) -> str:
        if " " in self._keyword:
            return f'"{self._keyword}"'
        else:
            return self._keyword
