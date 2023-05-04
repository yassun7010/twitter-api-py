from .operator import Operator


class IsNullcastOperator:
    def __invert__(self):
        return IsNotNullcastOperator()

    def __str__(self) -> str:
        return f"is:nullcast"


class IsNotNullcastOperator(Operator[Operator]):
    def __str__(self) -> str:
        return f"-is:nullcast"
