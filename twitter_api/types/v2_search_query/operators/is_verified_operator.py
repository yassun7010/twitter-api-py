from .operator import InvertableOperator, Operator


class IsVerifiedOperator(InvertableOperator[Operator]):
    def __str__(self) -> str:
        return f"is:verified"
