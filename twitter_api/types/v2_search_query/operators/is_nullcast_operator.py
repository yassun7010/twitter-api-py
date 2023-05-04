from .operator import Operator


class IsNullcastOperator:
    """
    Nullcast であるかどうか。

    否定形としてしか Operator として使えない。
    """

    def __invert__(self):
        return IsNotNullcastOperator()

    def __str__(self) -> str:
        return f"is:nullcast"


class IsNotNullcastOperator(Operator[Operator]):
    def __str__(self) -> str:
        return f"-is:nullcast"
