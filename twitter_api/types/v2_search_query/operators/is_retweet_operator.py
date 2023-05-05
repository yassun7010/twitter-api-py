from .operator import ConjunctionRequiredOperator, InvertibleOperator


class IsRetweetOperator(
    InvertibleOperator,
    ConjunctionRequiredOperator,
):
    def __str__(self) -> str:
        return "is:retweet"
