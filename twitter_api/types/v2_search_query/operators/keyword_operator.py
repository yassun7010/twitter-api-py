from twitter_api.error import SearchQueryDoubleQuotedError

from .operator import InvertibleOperator, StandaloneOperator


class KeywordOperator(
    InvertibleOperator,
    StandaloneOperator,
):
    def __init__(self, keyword: str) -> None:
        if count := keyword.count('"'):
            if count == 2 and keyword[0] == '"' and keyword[-1] == '"':
                self._keyword = keyword[1:-1]
                return

            raise SearchQueryDoubleQuotedError()

        self._keyword = keyword

    def __str__(self) -> str:
        if " " in self._keyword:
            return f'"{self._keyword}"'
        else:
            return self._keyword
