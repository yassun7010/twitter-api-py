from twitter_api.types.v2_search_query.operators.has_cashtags_operator import (
    HasCashtagsOperator,
)
from twitter_api.types.v2_search_query.search_query import SearchQuery


class TestHasCashtagsOperator:
    def test_has_cashtags_operator(self):
        assert str(HasCashtagsOperator()) == "has:cashtags"

    def test_query_build(self):
        assert str(SearchQuery.build(lambda q: q.has_cashtags())) == "has:cashtags"
