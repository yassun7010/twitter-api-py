from .operator import ConjunctionRequiredOperator, InvertibleOperator


class HasLinksOperator(
    InvertibleOperator,
    ConjunctionRequiredOperator,
):
    def __str__(self) -> str:
        return "has:links"
