from typing import Union, cast, overload


class Operator:
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({repr(str(self))})"


class CompleteOperator(Operator):
    """
    検索クエリとして成り立っている Operator。
    """

    def __and__(self, other: Operator):
        from ._and_operator import CompleteAndOperator

        return CompleteAndOperator(self, other)

    @overload
    def __or__(self, other: "CompleteOperator") -> "CompleteOperator":
        ...

    @overload
    def __or__(self, other: "IncompleteOperator") -> "IncompleteOperator":
        ...

    def __or__(self, other: Union["CompleteOperator", "IncompleteOperator"]):
        from ._or_operator import CompleteOrOperator, IncompleteOrOperator

        if isinstance(other, CompleteOperator):
            return cast(CompleteOperator, CompleteOrOperator(self, other))
        else:
            return cast(IncompleteOperator, IncompleteOrOperator(self, other))


class IncompleteOperator(Operator):
    """
    まだ検索クエリとして成り立たっていない Operator。
    """

    @overload
    def __and__(self, other: "CompleteOperator") -> "CompleteOperator":
        ...

    @overload
    def __and__(self, other: "IncompleteOperator") -> "IncompleteOperator":
        ...

    def __and__(self, other: Union["CompleteOperator", "IncompleteOperator"]):
        from ._and_operator import CompleteAndOperator, IncompleteAndOperator

        if isinstance(other, CompleteOperator):
            return cast(CompleteOperator, CompleteAndOperator(self, other))
        else:
            return cast(IncompleteOperator, IncompleteAndOperator(self, other))

    def __or__(self, other: Operator) -> "IncompleteOperator":
        from ._or_operator import IncompleteOrOperator

        return IncompleteOrOperator(self, other)


class InvertibleOperator(Operator):
    """
    否定（ ~ 演算子を適用）することのできる Operator。
    """

    def __invert__(self):
        from ._not_operator import NotOperator

        return NotOperator(self)


class ConjunctionRequiredOperator(IncompleteOperator):
    """
    Twitter が定義した、それ自身だけではクエリとして成立しない Operator。

    refer: https://developer.twitter.com/en/docs/twitter-api/tweets/search/integrate/build-a-query#list
    """

    pass


class StandaloneOperator(CompleteOperator):
    """
    Twitter が定義した、それ自身がクエリとして成立する Operator。

    refer: https://developer.twitter.com/en/docs/twitter-api/tweets/search/integrate/build-a-query#list
    """

    pass
