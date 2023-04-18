import pytest

from tests.data import json_test_data
from twitter_api.api.types.v2_tweet.tweet_response_body import TweetsSearchResponseBody


@pytest.fixture
def response() -> TweetsSearchResponseBody:
    return TweetsSearchResponseBody.parse_file(
        json_test_data("get_v2_tweets_search_recent_response_all_fields.json"),
    )


class TestTweetsSearchResponseBody:
    def test_find_tweet_by(
        self,
        response: TweetsSearchResponseBody,
    ):
        retweeted_tweet = response.find_tweet_by("1647123314605965312")

        assert retweeted_tweet is not None
        assert retweeted_tweet.id == "1647123314605965312"

    def test_find_retweeted_tweet_by(
        self,
        response: TweetsSearchResponseBody,
    ):
        retweeted_tweet = response.find_retweeted_tweet_by("1647123314605965312")

        assert retweeted_tweet is not None
        assert retweeted_tweet.id == "1647031756388962305"

    @pytest.mark.xfail(reason="同じレスポンスの中に引用元のツイートが存在しない。")
    def test_find_quoted_tweet_by(
        self,
        response: TweetsSearchResponseBody,
    ):
        quoted_tweet = response.find_quoted_tweet_by("1647121928971522048")

        assert quoted_tweet is not None
        assert quoted_tweet.id == "1647073612271321093"

    def test_find_replied_tweet_by(
        self,
        response: TweetsSearchResponseBody,
    ):
        replied_tweet = response.find_replied_tweet_by("1647123304380268545")

        assert replied_tweet is not None
        assert replied_tweet.id == "1647122898220621824"

    def test_find_mentioned_users_by(
        self,
        response: TweetsSearchResponseBody,
    ):
        mentioned_users = response.find_mentioned_users_by("1647123313993601026")

        assert [user.id for user in mentioned_users] == ["183584495"]
