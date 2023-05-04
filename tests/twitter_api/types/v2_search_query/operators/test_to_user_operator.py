from twitter_api.types.v2_search_query.operators.to_user_operator import ToUserOperator
from twitter_api.types.v2_search_query.search_query import SearchQuery


class TestToUserOperator:
    def test_to_user_operator(self):
        assert str(ToUserOperator("twitterdev")) == "to:twitterdev"

    def test_query_build(self):
        assert (
            str(SearchQuery.build(lambda q: q.to_user("twitterdev"))) == "to:twitterdev"
        )
