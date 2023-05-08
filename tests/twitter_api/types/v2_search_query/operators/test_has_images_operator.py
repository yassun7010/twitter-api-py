from twitter_api.types.v2_search_query.operators.has_images_operator import (
    HasImagesOperator,
)
from twitter_api.types.v2_search_query.operators.operator import IncompleteOperator
from twitter_api.types.v2_search_query.search_query import SearchQuery, build


class TestHasImagesOperator:
    def test_has_images_operator(self):
        assert str(HasImagesOperator()) == "has:images"

    def test_query_incomplete(self):
        assert isinstance(
            build(lambda q: q.has_images()),
            IncompleteOperator,
        )

    def test_query_build(self):
        assert (
            str(SearchQuery.build(lambda q: q.mention("twitterdev") & q.has_images()))
            == "@twitterdev has:images"
        )
