from .operator import ConjunctionRequiredOperator, InvertibleOperator


class HasGeoOperator(
    InvertibleOperator,
    ConjunctionRequiredOperator,
):
    def __str__(self) -> str:
        return "has:geo"
