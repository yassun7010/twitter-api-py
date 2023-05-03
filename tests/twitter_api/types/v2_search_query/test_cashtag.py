from twitter_api.types.v2_search_query.cashtag import Cashtag
from twitter_api.types.v2_search_query.search_query import SearchQuery


class TestCashtag:
    def test_cashtag(self):
        assert str(Cashtag("Twitter")) == "$Twitter"

    def test_cashtag_with_mark(self):
        assert str(Cashtag("$Twitter")) == "$Twitter"

    def test_query_build(self):
        assert str(SearchQuery.build(lambda q: q.cashtag("Twitter"))) == "$Twitter"
