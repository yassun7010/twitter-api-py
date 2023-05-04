from .operator import ConjunctionRequiredOperator, InvertableOperator, Operator


class HasVideoLinkOperator(
    InvertableOperator[Operator],
    ConjunctionRequiredOperator,
):
    def __str__(self) -> str:
        return "has:video_link"
