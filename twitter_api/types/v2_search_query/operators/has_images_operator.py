from .operator import Operator


class HasImagesOperator(Operator[Operator]):
    def __str__(self) -> str:
        return f"has:images"
