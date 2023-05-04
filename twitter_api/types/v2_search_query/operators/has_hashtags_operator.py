from .operator import ConjunctionRequiredOperator, InvertableOperator, Operator


class HasHashtagsOperator(
    InvertableOperator[Operator],
    ConjunctionRequiredOperator,
):
    def __str__(self) -> str:
        return f"has:hashtags"
