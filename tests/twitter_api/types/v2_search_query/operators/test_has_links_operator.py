from twitter_api.types.v2_search_query.operators.has_links_operator import (
    HasLinksOperator,
)
from twitter_api.types.v2_search_query.search_query import SearchQuery


class TestHasLinksOperator:
    def test_has_links_operator(self):
        assert str(HasLinksOperator()) == "has:links"

    def test_query_build(self):
        assert str(SearchQuery.build(lambda q: q.has_links())) == "has:links"
