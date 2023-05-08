from twitter_api.types.v2_search_query.operators.from_user_operator import (
    FromUserOperator,
)
from twitter_api.types.v2_search_query.operators.operator import CompleteOperator
from twitter_api.types.v2_search_query.search_query import SearchQuery, build


class TestFromUserOperator:
    def test_from_user_operator(self):
        assert str(FromUserOperator("twitterdev")) == "from:twitterdev"

    def test_query_complete(self):
        assert isinstance(
            build(lambda q: q.from_user("twitterdev")),
            CompleteOperator,
        )

    def test_query_build(self):
        assert (
            str(SearchQuery.build(lambda q: q.from_user("twitterdev")))
            == "from:twitterdev"
        )
