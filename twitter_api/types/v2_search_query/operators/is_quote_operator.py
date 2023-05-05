from .operator import ConjunctionRequiredOperator, InvertibleOperator, Operator


class IsQuoteOperator(
    InvertibleOperator[Operator],
    ConjunctionRequiredOperator,
):
    def __str__(self) -> str:
        return "is:quote"
