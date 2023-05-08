from twitter_api.types.v2_search_query.operators.operator import CompleteOperator
from twitter_api.types.v2_search_query.operators.retweets_of_operator import (
    RetweetsOfOperator,
)
from twitter_api.types.v2_search_query.search_query import SearchQuery, build


class TestRetweetsOfOperator:
    def test_retweets_of_operator(self):
        assert str(RetweetsOfOperator("twitterdev")) == "retweets_of:twitterdev"

    def test_query_complete(self):
        assert isinstance(
            build(lambda q: q.retweets_of("twitterdev")),
            CompleteOperator,
        )

    def test_query_build(self):
        assert (
            str(SearchQuery.build(lambda q: q.retweets_of("twitterdev")))
            == "retweets_of:twitterdev"
        )
