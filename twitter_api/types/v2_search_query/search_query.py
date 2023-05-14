from typing import Callable

from twitter_api.types.v2_search_query.operators.group_operator import GroupOperator
from twitter_api.types.v2_search_query.search_query_builder import SearchQueryBuilder

from .operators.operator import CompleteOperator, Operator


class SearchQuery:
    """
    検索クエリの作成をエディタの支援を受けながら行うためのクラス。

    SearchQuery.build を用いて作成する。

    refer: https://developer.twitter.com/en/docs/twitter-api/tweets/search/integrate/build-a-query
    """

    def __init__(self, query: Operator) -> None:
        self._query = query

    def __str__(self) -> str:
        # ルートが Group の場合は括弧で囲まない。
        if isinstance(self._query, GroupOperator):
            return str(self._query._operator)
        else:
            return str(self._query)

    def __repr__(self):
        return f"{self.__class__.__name__}({repr(self._query)})"

    @classmethod
    def build(
        cls,
        building: Callable[[SearchQueryBuilder], CompleteOperator],
    ):
        """
        検索クエリを組み立てる。

        静的解析でエラーを出さずにクエリを組み立てるには、下記のルールに従う。

        - AND 演算（ & 結合）は左右のどちらかがクエリとして成立する場合、結合結果もクエリとして成立する。
        - OR 演算（ | 結合）は左右の両方がクエリとして成立する場合、結合結果もクエリとして成立する。
        - NOT 演算（ ~ ）により否定された要素は、単体ではクエリとして成立しない。
        - グループで囲まれた要素は先に評価される。
        - 二重否定、グループへの否定はできない。

        >>> from .search_query import SearchQuery
        >>> query = SearchQuery.build(
        ...     lambda q: (
        ...         q.keyword("day")
        ...         & q.group(
        ...             q.hashtag("#Twitter") | q.hashtag("Xcorp"),
        ...         )
        ...         & q.mention("@elonmusk")
        ...         & ~q.mention("SpaceX")
        ...         & q.is_retweet()
        ...     )
        ... )
        >>> str(query)
        'day (#Twitter OR #Xcorp) @elonmusk -@SpaceX is:retweet'
        """

        return SearchQuery(build(building))


def build(building: Callable[[SearchQueryBuilder], Operator]) -> Operator:
    return building(SearchQueryBuilder())
