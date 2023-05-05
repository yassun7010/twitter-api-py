from .operator import ConjunctionRequiredOperator, InvertibleOperator


class HasHashtagsOperator(
    InvertibleOperator,
    ConjunctionRequiredOperator,
):
    def __str__(self) -> str:
        return "has:hashtags"
