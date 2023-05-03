from twitter_api.types.v2_search_query.from_user import FromUser
from twitter_api.types.v2_search_query.search_query import SearchQuery


class TestFromUser:
    def test_from_user(self):
        assert str(FromUser("twitterdev")) == "from:twitterdev"

    def test_from_user_with_mark(self):
        assert str(FromUser("from:twitterdev")) == "from:twitterdev"

    def test_query_build(self):
        assert (
            str(SearchQuery.build(lambda q: q.from_user("twitterdev")))
            == "from:twitterdev"
        )
