from .operator import ConjunctionRequiredOperator, InvertibleOperator, Operator


class HasCashtagsOperator(
    InvertibleOperator[Operator],
    ConjunctionRequiredOperator,
):
    def __str__(self) -> str:
        return "has:cashtags"
