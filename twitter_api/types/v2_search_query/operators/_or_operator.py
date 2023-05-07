from .operator import CompleteOperator, IncompleteOperator, Operator


class OrOperator(Operator):
    def __init__(self, left: Operator, right: Operator) -> None:
        self._left = left
        self._right = right

    def __str__(self) -> str:
        return f"{self._left} OR {self._right}"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({repr(self._left)}, {repr(self._right)})"


class CompleteOrOperator(OrOperator, CompleteOperator):
    def __init__(self, left: CompleteOperator, right: CompleteOperator) -> None:
        super().__init__(left, right)


class IncompleteOrOperator(OrOperator, IncompleteOperator):
    pass
