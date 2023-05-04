from .operator import InvertableOperator, Operator


class IsReplyOperator(InvertableOperator[Operator]):
    def __str__(self) -> str:
        return f"is:reply"
