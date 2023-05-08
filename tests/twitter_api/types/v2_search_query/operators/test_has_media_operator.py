from twitter_api.types.v2_search_query.operators.has_media_operator import (
    HasMediaOperator,
)
from twitter_api.types.v2_search_query.operators.operator import IncompleteOperator
from twitter_api.types.v2_search_query.search_query import SearchQuery, build


class TestHasMediaOperator:
    def test_has_media_operator(self):
        assert str(HasMediaOperator()) == "has:media"

    def test_query_incomplete(self):
        assert isinstance(build(lambda q: q.has_media()), IncompleteOperator)

    def test_query_build(self):
        assert (
            str(SearchQuery.build(lambda q: q.mention("twitterdev") & q.has_media()))
            == "@twitterdev has:media"
        )
