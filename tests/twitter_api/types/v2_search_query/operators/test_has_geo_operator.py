from twitter_api.types.v2_search_query.operators.has_geo_operator import HasGeoOperator
from twitter_api.types.v2_search_query.search_query import SearchQuery


class TestHasGeoOperator:
    def test_has_geo_operator(self):
        assert str(HasGeoOperator()) == "has:geo"

    def test_query_build(self):
        assert str(SearchQuery.build(lambda q: q.has_geo())) == "has:geo"
