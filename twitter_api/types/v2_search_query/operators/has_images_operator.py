from .operator import ConjunctionRequiredOperator, InvertibleOperator


class HasImagesOperator(
    InvertibleOperator,
    ConjunctionRequiredOperator,
):
    def __str__(self) -> str:
        return "has:images"
