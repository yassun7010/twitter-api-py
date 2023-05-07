from .operator import CompleteOperator, IncompleteOperator, Operator


class GroupOperator(
    # NOTE: 公式ドキュメントでは否定をグループに対して行わないように書かれており、
    #       "skiing -(snow OR day OR noschool)" よりも
    #       "skiing -snow -day -noschool" の方が推奨されている。
    #       そのため、本ツールではグループへの否定演算子は対応しない。
    #
    # refer: https://developer.twitter.com/en/docs/twitter-api/tweets/search/integrate/build-a-query
    #
    # InvertibleOperator,
    Operator,
):
    def __init__(self, operator: Operator):
        if isinstance(operator, GroupOperator):
            # GroupOperator の重ね掛けはまとめる。
            self._operator = operator._operator
        else:
            self._operator = operator

    def __str__(self) -> str:
        from ._and_operator import AndOperator
        from ._or_operator import OrOperator

        if isinstance(self._operator, (AndOperator, OrOperator)):
            return f"({self._operator})"

        else:
            return str(self._operator)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({repr(self._operator)})"


class IncompleteGroupOperator(GroupOperator, IncompleteOperator):
    pass


class CompleteGroupOperator(GroupOperator, CompleteOperator):
    def __init__(self, operator: CompleteOperator):
        super().__init__(operator)
