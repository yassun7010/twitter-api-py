from .operator import ConjunctionRequiredOperator, InvertibleOperator, Operator


class HasMentionsOperator(
    InvertibleOperator[Operator],
    ConjunctionRequiredOperator,
):
    def __str__(self) -> str:
        return "has:mentions"
