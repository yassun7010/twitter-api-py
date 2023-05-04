from .operator import InvertableOperator, Operator


class HasImagesOperator(InvertableOperator[Operator]):
    def __str__(self) -> str:
        return f"has:images"
