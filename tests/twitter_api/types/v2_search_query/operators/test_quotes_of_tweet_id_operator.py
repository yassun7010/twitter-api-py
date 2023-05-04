from twitter_api.types.v2_search_query.operators.quotes_of_tweet_id_operator import (
    QuotesOfTweetIdOperator,
)
from twitter_api.types.v2_search_query.search_query import SearchQuery


class TestQuotesOfTweetIdOperator:
    def test_quotes_of_tweet_id_operator(self):
        assert (
            str(QuotesOfTweetIdOperator("1539382664746020864"))
            == "quotes_of_tweet_id:1539382664746020864"
        )

    def test_query_build(self):
        assert (
            str(
                SearchQuery.build(lambda q: q.quotes_of_tweet_id("1539382664746020864"))
            )
            == "quotes_of_tweet_id:1539382664746020864"
        )
