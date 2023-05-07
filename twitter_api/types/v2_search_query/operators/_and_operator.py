from typing import overload

from .operator import CompleteOperator, IncompleteOperator, Operator


class AndOperator(Operator):
    def __init__(self, left: Operator, right: Operator) -> None:
        self._left = left
        self._right = right

    def __str__(self) -> str:
        return f"{self._left} {self._right}"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({repr(self._left)}, {repr(self._right)})"


class CompleteAndOperator(AndOperator, CompleteOperator):
    @overload
    def __init__(self, left: CompleteOperator, right: Operator) -> None:
        ...

    @overload
    def __init__(self, left: Operator, right: CompleteOperator) -> None:
        ...

    def __init__(self, left, right) -> None:
        self._left = left
        self._right = right


class IncompleteAndOperator(AndOperator, IncompleteOperator):
    pass
