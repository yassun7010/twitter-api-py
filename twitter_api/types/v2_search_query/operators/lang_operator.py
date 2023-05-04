from twitter_api.types.v2_language import Language

from .operator import ConjunctionRequiredOperator, InvertableOperator, Operator


class LangOperator(
    InvertableOperator[Operator],
    ConjunctionRequiredOperator,
):
    def __init__(self, lang: Language):
        self._value = lang

    def __str__(self) -> str:
        return f"lang:{self._value}"
