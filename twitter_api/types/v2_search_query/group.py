from twitter_api.types.v2_search_query.operator import Operator


class Group(Operator[Operator]):
    def __init__(self, *operators: Operator):
        if len(operators) == 1 and isinstance(operators[0], Group):
            self._operators = operators[0]._operators
        else:
            self._operators = operators

    def __len__(self) -> int:
        return len(self._operators)

    def __str__(self) -> str:
        from ._and import And
        from ._or import Or

        if len(self._operators) == 1 and isinstance(self._operators[0], (And, Or)):
            return f"({self._operators[0]})"

        return " ".join(map(grouping, self._operators))


def grouping(operator: Operator):
    if isinstance(operator, Group) and len(operator) > 1:
        return f"({operator})"
    else:
        return str(operator)
