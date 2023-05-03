from .operator import Operator


class KeywordOperator(Operator[Operator]):
    def __init__(self, keyword: str) -> None:
        self._keyword = keyword

    def __str__(self) -> str:
        if " " in self._keyword:
            keyword = self._keyword.replace('"', '\\"')
            return f'"{keyword}"'
        else:
            return self._keyword
