from .operator import InvertableOperator, Operator


class HasHashtagsOperator(InvertableOperator[Operator]):
    def __str__(self) -> str:
        return f"has:hashtags"
