from twitter_api.types.v2_search_query.retweets_of_tweet_id import RetweetsOfTweetId
from twitter_api.types.v2_search_query.search_query import SearchQuery


class TestInReplyToTweetId:
    def test_retweets_of_tweet_id(self):
        assert (
            str(RetweetsOfTweetId("1539382664746020864"))
            == "retweets_of_tweet_id:1539382664746020864"
        )

    def test_query_build(self):
        assert (
            str(
                SearchQuery.build(
                    lambda q: q.retweets_of_tweet_id("1539382664746020864")
                )
            )
            == "retweets_of_tweet_id:1539382664746020864"
        )
