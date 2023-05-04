from twitter_api.types.v2_search_query.operators.is_quote_operator import (
    IsQuoteOperator,
)
from twitter_api.types.v2_search_query.search_query import SearchQuery


class TestIsQuoteOperator:
    def test_is_quote_operator(self):
        assert str(IsQuoteOperator()) == "is:quote"

    def test_query_build(self):
        assert (
            str(SearchQuery.build(lambda q: q.mention("twitterdev") & q.is_quote()))
            == "@twitterdev is:quote"
        )
