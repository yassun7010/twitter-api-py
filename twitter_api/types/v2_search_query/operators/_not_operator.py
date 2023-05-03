from .group_operator import grouping
from .operator import Operator


class NotOperator(Operator[Operator]):
    def __init__(self, op: Operator) -> None:
        self._op = op

    def __str__(self) -> str:
        return f"-{grouping(self._op)}"
