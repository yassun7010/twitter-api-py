from twitter_api.types.v2_search_query.operators.has_images_operator import (
    HasImagesOperator,
)
from twitter_api.types.v2_search_query.search_query import SearchQuery


class TestHasImagesOperator:
    def test_has_images_operator(self):
        assert str(HasImagesOperator()) == "has:images"

    def test_query_build(self):
        assert str(SearchQuery.build(lambda q: q.has_images())) == "has:images"
