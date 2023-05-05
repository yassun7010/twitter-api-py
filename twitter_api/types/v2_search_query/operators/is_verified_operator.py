from .operator import ConjunctionRequiredOperator, InvertibleOperator


class IsVerifiedOperator(
    InvertibleOperator,
    ConjunctionRequiredOperator,
):
    def __str__(self) -> str:
        return "is:verified"
