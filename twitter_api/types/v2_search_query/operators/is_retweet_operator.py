from .operator import Operator


class IsRetweetOperator(Operator[Operator]):
    def __str__(self) -> str:
        return f"is:retweet"
