from .operator import ConjunctionRequiredOperator, InvertibleOperator


class HasCashtagsOperator(
    InvertibleOperator,
    ConjunctionRequiredOperator,
):
    def __str__(self) -> str:
        return "has:cashtags"
