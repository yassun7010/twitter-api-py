from .operator import ConjunctionRequiredOperator, InvertibleOperator


class IsReplyOperator(
    InvertibleOperator,
    ConjunctionRequiredOperator,
):
    def __str__(self) -> str:
        return "is:reply"
