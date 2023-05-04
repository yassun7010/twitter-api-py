from .operator import InvertableOperator, Operator


class HasMediaOperator(InvertableOperator[Operator]):
    def __str__(self) -> str:
        return f"has:media"
