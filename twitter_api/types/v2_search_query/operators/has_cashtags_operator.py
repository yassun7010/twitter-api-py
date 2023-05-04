from .operator import Operator


class HasCashtagsOperator(Operator[Operator]):
    def __str__(self) -> str:
        return f"has:cashtags"
