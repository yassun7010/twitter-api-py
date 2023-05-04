import pytest

from twitter_api.types.v2_search_query.operators.keyword_operator import KeywordOperator
from twitter_api.types.v2_search_query.operators.mention_operator import MentionOperator
from twitter_api.types.v2_search_query.search_query import (
    SearchQuery,
    _SearchQueryBuilder,
)


class TestSearchQuery:
    def test_search_query_operator(self):
        query = SearchQuery(
            KeywordOperator("twitter")
            & MentionOperator("elonmusk")
            & ~MentionOperator("SpaceX"),
        )

        assert str(query) == "twitter @elonmusk -@SpaceX"

    def test_search_query_comma_separator(self):
        query = SearchQuery(
            KeywordOperator("twitter"),
            MentionOperator("elonmusk"),
            ~MentionOperator("SpaceX"),
        )

        assert str(query) == "twitter @elonmusk -@SpaceX"


class TestSearchQueryBuilder:
    def test_constructor(self):
        with pytest.raises(TypeError):
            _SearchQueryBuilder()  # type: ignore

    def test_search_query_builder(self):
        query = SearchQuery.build(
            lambda q: (
                q.keyword("twitter") & q.mention("elonmusk") & ~q.mention("SpaceX")
            )
        )

        assert str(query) == "twitter @elonmusk -@SpaceX"

    def test_search_query_builder_with_group(self):
        query = SearchQuery.build(
            lambda q: (
                q.group(
                    q.hashtag("#Twitter") | q.hashtag("Xcorp"),
                )
                & q.mention("@elonmusk")
                & ~q.mention("SpaceX")
            )
        )

        assert str(query) == "(#Twitter OR #Xcorp) @elonmusk -@SpaceX"
