from .operator import ConjunctionRequiredOperator, InvertableOperator, Operator


class HasGeoOperator(
    InvertableOperator[Operator],
    ConjunctionRequiredOperator,
):
    def __str__(self) -> str:
        return "has:geo"
