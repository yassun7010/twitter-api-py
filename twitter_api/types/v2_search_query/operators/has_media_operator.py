from .operator import ConjunctionRequiredOperator, InvertibleOperator


class HasMediaOperator(
    InvertibleOperator,
    ConjunctionRequiredOperator,
):
    def __str__(self) -> str:
        return "has:media"
