from .operator import ConjunctionRequiredOperator, InvertableOperator, Operator


class IsRetweetOperator(
    InvertableOperator[Operator],
    ConjunctionRequiredOperator,
):
    def __str__(self) -> str:
        return f"is:retweet"
