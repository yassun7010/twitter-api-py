from twitter_api.types.v2_search_query.search_query import SearchQuery
from twitter_api.types.v2_search_query.to_user import ToUser


class TestToUser:
    def test_to_user(self):
        assert str(ToUser("twitterdev")) == "to:twitterdev"

    def test_to_user_with_mark(self):
        assert str(ToUser("to:twitterdev")) == "to:twitterdev"

    def test_query_build(self):
        assert (
            str(SearchQuery.build(lambda q: q.to_user("twitterdev"))) == "to:twitterdev"
        )
