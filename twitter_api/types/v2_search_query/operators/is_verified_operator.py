from .operator import ConjunctionRequiredOperator, InvertibleOperator, Operator


class IsVerifiedOperator(
    InvertibleOperator[Operator],
    ConjunctionRequiredOperator,
):
    def __str__(self) -> str:
        return "is:verified"
