from twitter_api.types.v2_search_query.operators.bounding_box_operator import (
    BoundingBoxOperator,
)
from twitter_api.types.v2_search_query.search_query import SearchQuery


class TestBoundingBoxOperator:
    def test_bounding_box_operator_when_radius_km(self):
        assert (
            str(
                BoundingBoxOperator(
                    west_longitude=-105.301758,
                    south_latitude=39.964069,
                    east_longitude=-105.178505,
                    north_latitude=40.09455,
                )
            )
            == "bounding_box:[-105.301758 39.964069 -105.178505 40.09455]"
        )

    def test_query_build(self):
        assert (
            str(
                SearchQuery.build(
                    lambda q: q.bounding_box(
                        west_longitude=-105.301758,
                        south_latitude=39.964069,
                        east_longitude=-105.178505,
                        north_latitude=40.09455,
                    )
                )
            )
            == "bounding_box:[-105.301758 39.964069 -105.178505 40.09455]"
        )
