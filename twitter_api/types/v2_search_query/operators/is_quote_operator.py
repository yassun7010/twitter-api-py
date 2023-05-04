from .operator import ConjunctionRequiredOperator, InvertableOperator, Operator


class IsQuoteOperator(
    InvertableOperator[Operator],
    ConjunctionRequiredOperator,
):
    def __str__(self) -> str:
        return f"is:quote"
