from .operator import InvertableOperator, Operator, StandaloneOperator


class KeywordOperator(
    InvertableOperator[Operator],
    StandaloneOperator[Operator],
):
    def __init__(self, keyword: str) -> None:
        self._keyword = keyword

    def __str__(self) -> str:
        if " " in self._keyword:
            keyword = self._keyword.replace('"', '\\"')
            return f'"{keyword}"'
        else:
            return self._keyword
