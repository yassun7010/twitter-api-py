from .operator import Operator


class HasLinksOperator(Operator[Operator]):
    def __str__(self) -> str:
        return f"has:links"
