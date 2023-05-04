from typing import Generic, TypeVar

TOperator = TypeVar("TOperator", bound="Operator")


class Operator:
    pass


class CorrectOperator(Operator, Generic[TOperator]):
    def __and__(self, other: TOperator):
        from ._and_operator import AndOperator

        return AndOperator(self, other)

    def __or__(self, other: "CorrectOperator"):
        from ._or_operator import OrOperator

        return OrOperator(self, other)


class InvertableOperator(Operator, Generic[TOperator]):
    def __invert__(self):
        from ._not_operator import NotOperator

        return NotOperator(self)


class StandaloneOperator(CorrectOperator[TOperator]):
    pass
