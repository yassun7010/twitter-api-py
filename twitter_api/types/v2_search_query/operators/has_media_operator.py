from .operator import ConjunctionRequiredOperator, InvertibleOperator, Operator


class HasMediaOperator(
    InvertibleOperator[Operator],
    ConjunctionRequiredOperator,
):
    def __str__(self) -> str:
        return "has:media"
