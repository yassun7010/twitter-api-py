from .operator import ConjunctionRequiredOperator, InvertableOperator, Operator


class HasLinksOperator(
    InvertableOperator[Operator],
    ConjunctionRequiredOperator,
):
    def __str__(self) -> str:
        return f"has:links"
