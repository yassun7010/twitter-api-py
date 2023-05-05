from .operator import ConjunctionRequiredOperator, InvertibleOperator


class IsQuoteOperator(
    InvertibleOperator,
    ConjunctionRequiredOperator,
):
    def __str__(self) -> str:
        return "is:quote"
