from .group_operator import grouping
from .operator import Operator


class AndOperator(Operator[Operator]):
    def __init__(self, left: Operator, right: Operator) -> None:
        self._left = left
        self._right = right

    def __str__(self) -> str:
        return f"{grouping(self._left)} {grouping(self._right)}"
