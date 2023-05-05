from .operator import ConjunctionRequiredOperator, InvertibleOperator, Operator


class HasImagesOperator(
    InvertibleOperator[Operator],
    ConjunctionRequiredOperator,
):
    def __str__(self) -> str:
        return "has:images"
