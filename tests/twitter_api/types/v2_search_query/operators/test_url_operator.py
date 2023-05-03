from twitter_api.types.v2_search_query.operators.url_operator import UrlOperator
from twitter_api.types.v2_search_query.search_query import SearchQuery


class TestUrl:
    def test_url(self):
        assert str(UrlOperator("https://google.com")) == 'url:"https://google.com"'

    def test_query_build(self):
        assert (
            str(SearchQuery.build(lambda q: q.url("https://google.com")))
            == 'url:"https://google.com"'
        )
