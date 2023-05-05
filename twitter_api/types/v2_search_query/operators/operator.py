from typing import Union, cast, overload


class Operator:
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({repr(str(self))})"


class WeakOperator(Operator):
    """
    まだ検索クエリとして成り立たっていない Operator。
    """

    @overload
    def __and__(self, other: "CorrectOperator") -> "CorrectOperator":
        ...

    @overload
    def __and__(self, other: Operator) -> "WeakOperator":
        ...

    def __and__(self, other: Union["CorrectOperator", Operator]):
        from ._and_operator import CorrectAndOperator, WeakAndOperator

        if isinstance(other, CorrectOperator):
            return cast(CorrectOperator, CorrectAndOperator(self, other))
        else:
            return cast(WeakOperator, WeakAndOperator(self, other))

    def __or__(self, other: Operator):
        from ._or_operator import WeakOrOperator

        return WeakOrOperator(self, other)


class CorrectOperator(Operator):
    """
    検索クエリとして成り立つことのできる Operator。
    """

    def __and__(self, other: Operator):
        from ._and_operator import CorrectAndOperator

        return CorrectAndOperator(self, other)

    @overload
    def __or__(self, other: "CorrectOperator") -> "CorrectOperator":
        ...

    @overload
    def __or__(self, other: Operator) -> WeakOperator:
        ...

    def __or__(self, other: Union["CorrectOperator", Operator]):
        from ._or_operator import CorrectOrOperator, WeakOrOperator

        if isinstance(other, CorrectOperator):
            return cast(CorrectOperator, CorrectOrOperator(self, other))
        else:
            return cast(WeakOperator, WeakOrOperator(self, other))


class InvertibleOperator(Operator):
    """
    否定（ ~ 演算子を追加）することのできる Operator。
    """

    def __invert__(self):
        from ._not_operator import NotOperator

        return NotOperator(self)


class ConjunctionRequiredOperator(WeakOperator):
    """
    自身だけではクエリとして成立しない Operator。

    refer: https://developer.twitter.com/en/docs/twitter-api/tweets/search/integrate/build-a-query#list
    """

    pass


class StandaloneOperator(CorrectOperator):
    """
    それ自身がクエリとして成立する Operator。

    refer: https://developer.twitter.com/en/docs/twitter-api/tweets/search/integrate/build-a-query#list
    """

    pass
