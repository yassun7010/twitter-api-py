from .group_operator import grouping
from .operator import CorrectOperator, Operator


class AndOperator(CorrectOperator[Operator]):
    def __init__(self, left: CorrectOperator, right: Operator) -> None:
        self._left = left
        self._right = right

    def __str__(self) -> str:
        return f"{grouping(self._left)} {grouping(self._right)}"
