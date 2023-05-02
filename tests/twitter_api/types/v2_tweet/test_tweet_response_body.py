import pytest

from tests.data import json_test_data
from twitter_api.types.v2_tweet.tweet_response_body import TweetsSearchResponseBody


@pytest.fixture
def response() -> TweetsSearchResponseBody:
    return TweetsSearchResponseBody.parse_file(
        json_test_data("get_v2_tweets_search_recent/collected_response_body.json"),
    )


class TestTweetsSearchResponseBody:
    def test_find_tweet_by(
        self,
        response: TweetsSearchResponseBody,
    ):
        retweeted_tweet = response.find_tweet_by("1648980229258612736")

        assert retweeted_tweet is not None
        assert retweeted_tweet.id == "1648980229258612736"

    def test_find_retweeted_tweet_by(
        self,
        response: TweetsSearchResponseBody,
    ):
        retweeted_tweet = response.find_retweeted_tweet_by("1648955380469317634")

        assert retweeted_tweet is not None
        assert retweeted_tweet.id == "1648303577893412865"

    def test_find_quoted_tweet_by(
        self,
        response: TweetsSearchResponseBody,
    ):
        quoted_tweet = response.find_quoted_tweet_by("1648702929942052865")

        assert quoted_tweet is not None
        assert quoted_tweet.id == "1648387817490493441"

    def test_find_replied_tweet_by(
        self,
        response: TweetsSearchResponseBody,
    ):
        replied_tweet = response.find_replied_tweet_by("1648220109431865346")

        assert replied_tweet is not None
        assert replied_tweet.id == "1648209168766054401"

    def test_find_mentioned_users_by(
        self,
        response: TweetsSearchResponseBody,
    ):
        mentioned_users = response.find_mentioned_users_by("1648220109431865346")

        assert [user.id for user in mentioned_users] == ["128262047"]
