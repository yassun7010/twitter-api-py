from .operator import ConjunctionRequiredOperator, InvertibleOperator, Operator


class HasGeoOperator(
    InvertibleOperator[Operator],
    ConjunctionRequiredOperator,
):
    def __str__(self) -> str:
        return "has:geo"
