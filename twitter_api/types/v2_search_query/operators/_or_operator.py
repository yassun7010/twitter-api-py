from .group_operator import grouping
from .operator import CorrectOperator, Operator


class OrOperator(CorrectOperator[Operator]):
    def __init__(self, left: CorrectOperator, right: CorrectOperator) -> None:
        self._left = left
        self._right = right

    def __str__(self) -> str:
        return f"{grouping(self._left)} OR {grouping(self._right)}"

    def __repr__(self):
        return f"{self.__class__.__name__}({repr(self._left)}, {repr(self._right)})"
