from .operator import Operator


class IsReplyOperator(Operator[Operator]):
    def __str__(self) -> str:
        return f"is:reply"
