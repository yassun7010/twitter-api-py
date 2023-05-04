from .operator import InvertableOperator, Operator


class HasLinksOperator(InvertableOperator[Operator]):
    def __str__(self) -> str:
        return f"has:links"
