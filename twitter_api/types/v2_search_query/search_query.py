from typing import Any

from twitter_api.types.v2_search_query.group import grouping
from twitter_api.types.v2_search_query.operator import Operator


class SearchQuery:
    def __init__(self, *query: Operator[Any]) -> None:
        self._query = query

    def __str__(self) -> str:
        return " ".join(map(grouping, self._query))
