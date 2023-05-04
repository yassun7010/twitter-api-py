from .operator import InvertableOperator, Operator


class IsRetweetOperator(InvertableOperator[Operator]):
    def __str__(self) -> str:
        return f"is:retweet"
