from twitter_api.types.v2_search_query.quotes_of_tweet_id import QuotesOfTweetId
from twitter_api.types.v2_search_query.search_query import SearchQuery


class TestQuotesOfTweetId:
    def test_quotes_of_tweet_id(self):
        assert (
            str(QuotesOfTweetId("1539382664746020864"))
            == "quotes_of_tweet_id:1539382664746020864"
        )

    def test_query_build(self):
        assert (
            str(
                SearchQuery.build(lambda q: q.quotes_of_tweet_id("1539382664746020864"))
            )
            == "quotes_of_tweet_id:1539382664746020864"
        )
