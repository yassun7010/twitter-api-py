from .operator import Operator


class HasMentionsOperator(Operator[Operator]):
    def __str__(self) -> str:
        return f"has:mentions"
