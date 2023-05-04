from .operator import Operator


class HasHashtagsOperator(Operator[Operator]):
    def __str__(self) -> str:
        return f"has:hashtags"
