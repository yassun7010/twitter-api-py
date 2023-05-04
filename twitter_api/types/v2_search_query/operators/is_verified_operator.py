from .operator import ConjunctionRequiredOperator, InvertableOperator, Operator


class IsVerifiedOperator(
    InvertableOperator[Operator],
    ConjunctionRequiredOperator,
):
    def __str__(self) -> str:
        return f"is:verified"
