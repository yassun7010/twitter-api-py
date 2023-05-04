from .operator import Operator


class HasMediaOperator(Operator[Operator]):
    def __str__(self) -> str:
        return f"has:media"
