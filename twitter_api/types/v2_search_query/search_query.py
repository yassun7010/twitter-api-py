from abc import abstractmethod
from typing import Any, Callable, Self, Type, Union

from twitter_api.types.v2_search_query.group import Group, grouping
from twitter_api.types.v2_search_query.hashtag import Hashtag
from twitter_api.types.v2_search_query.keyword import Keyword
from twitter_api.types.v2_search_query.mention import Mention
from twitter_api.types.v2_search_query.operator import Operator
from twitter_api.types.v2_user.username import Username


class SearchQuery:
    def __init__(self, *query: Operator[Any]) -> None:
        self._query = query

    def __str__(self) -> str:
        return " ".join(map(grouping, self._query))

    @classmethod
    def build(
        cls,
        building: Callable[
            [Type["_SearchQueryBuilder"]],
            Union[tuple[Operator[Any], ...], Operator[Any]],
        ],
    ):
        query = building(_SearchQueryBuilder)
        if isinstance(query, tuple):
            return SearchQuery(*query)
        else:
            return SearchQuery(query)


class _SearchQueryBuilder:
    @abstractmethod
    def __init__(self) -> None:
        pass

    @classmethod
    def keyword(cls, keyword: str) -> Keyword:
        return Keyword(keyword)

    @classmethod
    def mention(cls, username: Username) -> Mention:
        return Mention(username)

    @classmethod
    def hashtag(cls, hashtag: str) -> Hashtag:
        return Hashtag(hashtag)

    @classmethod
    def group(
        cls,
        operation: Callable[
            [Type[Self]], Union[tuple[Operator[Any], ...], Operator[Any]]
        ],
    ) -> Group:
        operators = operation(cls)
        if isinstance(operators, tuple):
            return Group(*operators)
        else:
            return Group(operators)
