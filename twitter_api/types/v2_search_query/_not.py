from twitter_api.types.v2_search_query.group import grouping
from twitter_api.types.v2_search_query.operator import Operator


class Not(Operator[Operator]):
    def __init__(self, op: Operator) -> None:
        self._op = op

    def __str__(self) -> str:
        return f"-{grouping(self._op)}"
