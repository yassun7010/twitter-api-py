from .operator import ConjunctionRequiredOperator, InvertableOperator, Operator


class IsReplyOperator(
    InvertableOperator[Operator],
    ConjunctionRequiredOperator,
):
    def __str__(self) -> str:
        return f"is:reply"
