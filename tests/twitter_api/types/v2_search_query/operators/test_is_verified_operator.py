from twitter_api.types.v2_search_query.operators.is_verified_operator import (
    IsVerifiedOperator,
)
from twitter_api.types.v2_search_query.search_query import SearchQuery


class TestIsVerifiedOperator:
    def test_is_verified_operator(self):
        assert str(IsVerifiedOperator()) == "is:verified"

    def test_query_build(self):
        assert str(SearchQuery.build(lambda q: q.is_verified())) == "is:verified"
