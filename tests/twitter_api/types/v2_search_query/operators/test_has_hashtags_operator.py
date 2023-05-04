from twitter_api.types.v2_search_query.operators.has_hashtags_operator import (
    HasHashtagsOperator,
)
from twitter_api.types.v2_search_query.search_query import SearchQuery


class TestHasHashtagsOperator:
    def test_has_hashtags_operator(self):
        assert str(HasHashtagsOperator()) == "has:hashtags"

    def test_query_build(self):
        assert str(SearchQuery.build(lambda q: q.has_hashtags())) == "has:hashtags"
