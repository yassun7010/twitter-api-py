from twitter_api.types.v2_search_query.in_reply_to_tweet_id import InReplyToTweetId
from twitter_api.types.v2_search_query.search_query import SearchQuery


class TestInReplyToTweetId:
    def test_in_reply_to_tweet_id(self):
        assert (
            str(InReplyToTweetId("1539382664746020864"))
            == "in_reply_to_tweet_id:1539382664746020864"
        )

    def test_query_build(self):
        assert (
            str(
                SearchQuery.build(
                    lambda q: q.in_reply_to_tweet_id("1539382664746020864")
                )
            )
            == "in_reply_to_tweet_id:1539382664746020864"
        )
