from .operator import ConjunctionRequiredOperator, InvertibleOperator, Operator


class HasLinksOperator(
    InvertibleOperator[Operator],
    ConjunctionRequiredOperator,
):
    def __str__(self) -> str:
        return "has:links"
