from twitter_api.types.v2_search_query.operators.group_operator import (
    CorrectGroupOperator,
    WeakGroupOperator,
)
from twitter_api.types.v2_search_query.search_query import SearchQuery, build


class TestGroupOperator:
    def test_group_operator_single_operator(self):
        query = SearchQuery.build(lambda q: q.group(q.mention("SpaceX")))

        assert str(query) == "@SpaceX"

    def test_group_operator_and_operator(self):
        query = SearchQuery.build(
            lambda q: (
                q.group(
                    q.keyword("twitter") & q.mention("twitterdev"),
                )
                & ~q.mention("SpaceX")
            )
        )
        assert str(query) == "(twitter @twitterdev) -@SpaceX"

    def test_group_operator_root_group(self):
        query = SearchQuery.build(
            lambda q: q.group(q.keyword("twitter") & q.mention("twitterdev"))
        )

        assert str(query) == "twitter @twitterdev"

    def test_search_query_builder_correct_group(self):
        query = build(
            lambda q: (
                q.group(
                    q.keyword("twitter") & q.mention("twitterdev"),
                )
            )
        )

        assert str(query) == "(twitter @twitterdev)"
        assert isinstance(query, CorrectGroupOperator)

    def test_search_query_builder_weak_group(self):
        query = build(
            lambda q: (
                q.group(
                    q.is_quote() | q.is_reply() | q.is_retweet(),
                )
            )
        )

        assert str(query) == "(is:quote OR is:reply OR is:retweet)"
        assert isinstance(query, WeakGroupOperator)
