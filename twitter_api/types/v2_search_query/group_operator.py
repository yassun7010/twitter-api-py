from twitter_api.types.v2_search_query.operator import Operator


class GroupOperator(Operator[Operator]):
    def __init__(self, *operators: Operator):
        if len(operators) == 1 and isinstance(operators[0], GroupOperator):
            # GroupOperator の重ね掛けはまとめる。
            self._operators = operators[0]._operators
        else:
            self._operators = operators

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
