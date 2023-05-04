from typing import Generic, TypeVar

TOperator = TypeVar("TOperator", bound="Operator")


class Operator:
    pass


class CorrectOperator(Operator, Generic[TOperator]):
    """
    検索クエリとして成り立つことのできる Operator。
    """

    def __and__(self, other: TOperator):
        from ._and_operator import AndOperator

        return AndOperator(self, other)

    def __or__(self, other: "CorrectOperator"):
        from ._or_operator import OrOperator

        return OrOperator(self, other)


class InvertableOperator(Operator, Generic[TOperator]):
    """
    否定（ ~ 演算子を追加）することのできる Operator。
    """

    def __invert__(self):
        from ._not_operator import NotOperator

        return NotOperator(self)


class ConjunctionRequiredOperator(Operator):
    """
    自身だけではクエリとして成立しない Operator。
    """

    pass


class StandaloneOperator(CorrectOperator[TOperator]):
    """
    それ自身がクエリとして成立する Operator。
    """

    pass
