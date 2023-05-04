from .operator import Operator


class HasGeoOperator(Operator[Operator]):
    def __str__(self) -> str:
        return f"has:geo"
