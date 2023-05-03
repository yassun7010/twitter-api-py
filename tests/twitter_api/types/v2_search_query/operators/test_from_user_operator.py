from twitter_api.types.v2_search_query.operators.from_user_operator import (
    FromUserOperator,
)
from twitter_api.types.v2_search_query.search_query import SearchQuery


class TestFromUser:
    def test_from_user(self):
        assert str(FromUserOperator("twitterdev")) == "from:twitterdev"

    def test_query_build(self):
        assert (
            str(SearchQuery.build(lambda q: q.from_user("twitterdev")))
            == "from:twitterdev"
        )
