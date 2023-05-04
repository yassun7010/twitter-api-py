from .operator import Operator


class HasVideoLinkOperator(Operator[Operator]):
    def __str__(self) -> str:
        return f"has:video_link"
