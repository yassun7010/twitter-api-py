from twitter_api.types.v2_search_query.retweet_of import RetweetOf
from twitter_api.types.v2_search_query.search_query import SearchQuery


class TestRetweetOf:
    def test_retweet_of(self):
        assert str(RetweetOf("twitterdev")) == "retweets_of:twitterdev"

    def test_retweet_of_with_mark(self):
        assert str(RetweetOf("retweets_of:twitterdev")) == "retweets_of:twitterdev"

    def test_query_build(self):
        assert (
            str(SearchQuery.build(lambda q: q.retweet_of("twitterdev")))
            == "retweets_of:twitterdev"
        )
