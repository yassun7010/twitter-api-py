from .operator import ConjunctionRequiredOperator, InvertibleOperator


class HasMentionsOperator(
    InvertibleOperator,
    ConjunctionRequiredOperator,
):
    def __str__(self) -> str:
        return "has:mentions"
