from .operator import ConjunctionRequiredOperator, InvertibleOperator, Operator


class HasVideoLinkOperator(
    InvertibleOperator[Operator],
    ConjunctionRequiredOperator,
):
    def __str__(self) -> str:
        return "has:video_link"
