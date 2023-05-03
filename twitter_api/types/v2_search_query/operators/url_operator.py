from .operator import Operator


class UrlOperator(Operator[Operator]):
    def __init__(self, url: str):
        self._value = url

    def __str__(self) -> str:
        return f'url:"{self._value}"'
