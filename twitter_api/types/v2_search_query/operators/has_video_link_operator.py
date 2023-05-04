from .operator import InvertableOperator, Operator


class HasVideoLinkOperator(InvertableOperator[Operator]):
    def __str__(self) -> str:
        return f"has:video_link"
