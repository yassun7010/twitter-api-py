from typing import Generic, TypeVar

TOperator = TypeVar("TOperator", bound="Operator")


class Operator(Generic[TOperator]):
    def __and__(self, other: TOperator):
        from ._and import And

        return And(self, other)

    def __or__(self, other: TOperator):
        from ._or import Or

        return Or(self, other)

    def __invert__(self):
        from ._not import Not

        return Not(self)
