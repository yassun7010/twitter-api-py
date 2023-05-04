from .operator import Operator


class IsNullcastOperator(Operator[Operator]):
    def __str__(self) -> str:
        return f"is:nullcast"
