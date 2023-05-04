from .operator import InvertableOperator, Operator


class HasGeoOperator(InvertableOperator[Operator]):
    def __str__(self) -> str:
        return f"has:geo"
