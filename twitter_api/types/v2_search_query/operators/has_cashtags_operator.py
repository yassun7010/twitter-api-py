from .operator import ConjunctionRequiredOperator, InvertableOperator, Operator


class HasCashtagsOperator(
    InvertableOperator[Operator],
    ConjunctionRequiredOperator,
):
    def __str__(self) -> str:
        return f"has:cashtags"
