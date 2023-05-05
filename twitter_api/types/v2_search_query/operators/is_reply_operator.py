from .operator import ConjunctionRequiredOperator, InvertibleOperator, Operator


class IsReplyOperator(
    InvertibleOperator[Operator],
    ConjunctionRequiredOperator,
):
    def __str__(self) -> str:
        return "is:reply"
