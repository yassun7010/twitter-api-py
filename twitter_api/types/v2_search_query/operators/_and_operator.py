from typing import overload

from .operator import CorrectOperator, Operator, WeakOperator


class AndOperator(Operator):
    def __init__(self, left: Operator, right: Operator) -> None:
        self._left = left
        self._right = right

    def __str__(self) -> str:
        return f"{self._left} {self._right}"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({repr(self._left)}, {repr(self._right)})"


class WeakAndOperator(AndOperator, WeakOperator):
    pass


class CorrectAndOperator(AndOperator, CorrectOperator):
    @overload
    def __init__(self, left: CorrectOperator, right: Operator) -> None:
        ...

    @overload
    def __init__(self, left: Operator, right: CorrectOperator) -> None:
        ...

    def __init__(self, left, right) -> None:
        self._left = left
        self._right = right
