from .operator import Operator


class IsVerifiedOperator(Operator[Operator]):
    def __str__(self) -> str:
        return f"is:verified"
