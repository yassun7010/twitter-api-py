from twitter_api.types.v2_search_query.operators.has_links_operator import (
    HasLinksOperator,
)
from twitter_api.types.v2_search_query.operators.operator import IncompleteOperator
from twitter_api.types.v2_search_query.search_query import SearchQuery, build


class TestHasLinksOperator:
    def test_has_links_operator(self):
        assert str(HasLinksOperator()) == "has:links"

    def test_query_incomplete(self):
        assert isinstance(
            build(lambda q: q.has_links()),
            IncompleteOperator,
        )

    def test_query_build(self):
        assert (
            str(SearchQuery.build(lambda q: q.mention("twitterdev") & q.has_links()))
            == "@twitterdev has:links"
        )
