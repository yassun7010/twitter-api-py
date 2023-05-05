from .operator import InvertibleOperator, StandaloneOperator


class UrlOperator(
    InvertibleOperator,
    StandaloneOperator,
):
    def __init__(self, url: str):
        self._value = url

    def __str__(self) -> str:
        return f'url:"{self._value}"'
