from twitter_api.types.v2_search_query.operators.is_retweet_operator import (
    IsRetweetOperator,
)
from twitter_api.types.v2_search_query.operators.operator import IncompleteOperator
from twitter_api.types.v2_search_query.search_query import SearchQuery, build


class TestIsRetweetOperator:
    def test_is_retweet_operator(self):
        assert str(IsRetweetOperator()) == "is:retweet"

    def test_query_incomplete(self):
        assert isinstance(build(lambda q: q.is_retweet()), IncompleteOperator)

    def test_query_build(self):
        assert (
            str(SearchQuery.build(lambda q: q.mention("twitterdev") & q.is_retweet()))
            == "@twitterdev is:retweet"
        )
