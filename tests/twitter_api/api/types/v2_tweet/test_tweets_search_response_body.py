import pytest

from tests.data import json_test_data
from twitter_api.api.types.v2_tweet.tweets_search_response_body import (
    TweetsSearchResponseBody,
)


@pytest.fixture
def response() -> TweetsSearchResponseBody:
    return TweetsSearchResponseBody.parse_file(
        json_test_data("get_v2_tweets_search_recent_response_all_fields.json"),
    )


class TestTweetsSearchResponseBody:
    def test_get_retweeted_tweet(
        self,
        response: TweetsSearchResponseBody,
    ):
        retweet = response.find_tweet("1647123314605965312")
        assert retweet is not None

        retweeted_tweet = response.retweeted_by(retweet)

        assert retweeted_tweet is not None
        assert retweeted_tweet.id == "1647031756388962305"

    @pytest.mark.skip("同じレスポンスの中に引用元のツイートが存在しない。")
    def test_get_quoted_tweet(
        self,
        response: TweetsSearchResponseBody,
    ):
        quote_tweet = response.find_tweet("1647031756388962305")
        assert quote_tweet is not None

        quoted_tweet = response.quoted_by(quote_tweet)

        assert quoted_tweet is None

    def test_get_replied_tweet(
        self,
        response: TweetsSearchResponseBody,
    ):
        reply_tweet = response.find_tweet("1647123304380268545")
        assert reply_tweet is not None

        replied_tweet = response.replied_by(reply_tweet)

        assert replied_tweet is not None
        assert replied_tweet.id == "1647122898220621824"

    def test_get_mentioned_users(
        self,
        response: TweetsSearchResponseBody,
    ):
        reply_tweet = response.find_tweet("1647123304380268545")
        assert reply_tweet is not None

        replied_tweet = response.replied_by(reply_tweet)

        assert replied_tweet is not None
        assert replied_tweet.id == "1647122898220621824"
