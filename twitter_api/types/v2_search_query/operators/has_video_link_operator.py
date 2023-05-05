from .operator import ConjunctionRequiredOperator, InvertibleOperator


class HasVideoLinkOperator(
    InvertibleOperator,
    ConjunctionRequiredOperator,
):
    def __str__(self) -> str:
        return "has:video_link"
