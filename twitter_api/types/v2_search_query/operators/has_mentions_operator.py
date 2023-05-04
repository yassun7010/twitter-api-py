from .operator import InvertableOperator, Operator


class HasMentionsOperator(InvertableOperator[Operator]):
    def __str__(self) -> str:
        return f"has:mentions"
