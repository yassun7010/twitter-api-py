from .operator import ConjunctionRequiredOperator, InvertableOperator, Operator


class HasMentionsOperator(
    InvertableOperator[Operator],
    ConjunctionRequiredOperator,
):
    def __str__(self) -> str:
        return f"has:mentions"
