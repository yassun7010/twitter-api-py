from .operator import ConjunctionRequiredOperator, InvertableOperator, Operator


class HasImagesOperator(
    InvertableOperator[Operator],
    ConjunctionRequiredOperator,
):
    def __str__(self) -> str:
        return "has:images"
