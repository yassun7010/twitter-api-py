from .operator import InvertableOperator, Operator


class HasCashtagsOperator(InvertableOperator[Operator]):
    def __str__(self) -> str:
        return f"has:cashtags"
