from twitter_api.types.v2_search_query.operators.in_reply_to_tweet_id_operator import (
    InReplyToTweetIdOperator,
)
from twitter_api.types.v2_search_query.search_query import SearchQuery


class TestInReplyToTweetId:
    def test_in_reply_to_tweet_id(self):
        assert (
            str(InReplyToTweetIdOperator("1539382664746020864"))
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
