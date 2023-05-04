from twitter_api.types.v2_search_query.operators.is_retweet_operator import (
    IsRetweetOperator,
)
from twitter_api.types.v2_search_query.search_query import SearchQuery


class TestIsRetweetOperator:
    def test_is_retweet_operator(self):
        assert str(IsRetweetOperator()) == "is:retweet"

    def test_query_build(self):
        assert str(SearchQuery.build(lambda q: q.is_retweet())) == "is:retweet"
