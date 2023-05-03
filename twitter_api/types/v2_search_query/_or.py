from twitter_api.types.v2_search_query.group import grouping
from twitter_api.types.v2_search_query.operator import Operator


class Or(Operator[Operator]):
    def __init__(self, left: Operator, right: Operator) -> None:
        self._left = left
        self._right = right

    def __str__(self) -> str:
        return f"{grouping(self._left)} OR {grouping(self._right)}"
