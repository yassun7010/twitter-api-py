from itertools import chain

from .operator import CorrectOperator, Operator


class GroupOperator(
    # NOTE: 公式ドキュメントでは否定をグループに対して行わないように書かれており、
    #       "skiing -(snow OR day OR noschool)" よりも
    #       "skiing -snow -day -noschool" の方が推奨されている。
    #       そのため、本ツールではグループへの否定演算子は対応しない。
    #
    # refer: https://developer.twitter.com/en/docs/twitter-api/tweets/search/integrate/build-a-query
    #
    # InvertableOperator[Operator],
    CorrectOperator[Operator],
):
    def __init__(self, operator: CorrectOperator, *operators: Operator):
        if len(operators) == 0 and isinstance(operator, GroupOperator):
            # GroupOperator の重ね掛けはまとめる。
            self._operators = operator._operators
        else:
            self._operators = tuple(chain((operator,), operators))

    def __len__(self) -> int:
        return len(self._operators)

    def __str__(self) -> str:
        from ._and_operator import AndOperator
        from ._not_operator import NotOperator
        from ._or_operator import OrOperator

        if len(self._operators) == 1 and isinstance(
            self._operators[0], (AndOperator, OrOperator, NotOperator)
        ):
            return f"({self._operators[0]})"

        return " ".join(map(grouping, self._operators))


def grouping(operator: Operator):
    if isinstance(operator, GroupOperator) and len(operator) > 1:
        return f"({operator})"
    else:
        return str(operator)
