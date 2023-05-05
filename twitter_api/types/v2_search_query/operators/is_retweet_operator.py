from .operator import ConjunctionRequiredOperator, InvertibleOperator, Operator


class IsRetweetOperator(
    InvertibleOperator[Operator],
    ConjunctionRequiredOperator,
):
    def __str__(self) -> str:
        return "is:retweet"
