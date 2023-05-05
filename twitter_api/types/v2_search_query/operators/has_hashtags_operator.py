from .operator import ConjunctionRequiredOperator, InvertibleOperator, Operator


class HasHashtagsOperator(
    InvertibleOperator[Operator],
    ConjunctionRequiredOperator,
):
    def __str__(self) -> str:
        return "has:hashtags"
