from twitter_api.types.v2_search_query.operators.place_country_operator import (
    PlaceCountryOperator,
)
from twitter_api.types.v2_search_query.search_query import SearchQuery


class TestPlaceCountryOperator:
    def test_place_country_operator(self):
        assert str(PlaceCountryOperator("US")) == "place_country:US"

    def test_query_build(self):
        assert (
            str(SearchQuery.build(lambda q: q.place_country("US")))
            == "place_country:US"
        )
