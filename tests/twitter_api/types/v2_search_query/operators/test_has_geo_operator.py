from twitter_api.types.v2_search_query.operators.has_geo_operator import HasGeoOperator
from twitter_api.types.v2_search_query.operators.operator import IncompleteOperator
from twitter_api.types.v2_search_query.search_query import SearchQuery, build


class TestHasGeoOperator:
    def test_has_geo_operator(self):
        assert str(HasGeoOperator()) == "has:geo"

    def test_query_incomplete(self):
        assert isinstance(
            build(lambda q: q.has_geo()),
            IncompleteOperator,
        )

    def test_query_build(self):
        assert (
            str(SearchQuery.build(lambda q: q.mention("twitterdev") & q.has_geo()))
            == "@twitterdev has:geo"
        )
