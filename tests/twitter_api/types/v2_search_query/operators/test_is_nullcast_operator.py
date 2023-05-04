from twitter_api.types.v2_search_query.operators.is_nullcast_operator import (
    IsNullcastOperator,
)
from twitter_api.types.v2_search_query.search_query import SearchQuery


class TestIsNullcastOperator:
    def test_is_nullcast_operator(self):
        assert str(IsNullcastOperator()) == "is:nullcast"

    def test_query_build(self):
        assert str(SearchQuery.build(lambda q: q.is_nullcast())) == "is:nullcast"
