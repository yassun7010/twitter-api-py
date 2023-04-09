from textwrap import dedent

import pytest

from tests.conftest import synthetic_monitoring_is_disable
from twitter_api.api.resources.v2_tweets.get_v2_tweets import GetV2TweetsResponseBody
from twitter_api.api.types.v2_tweet.tweet_detail import TweetDetail
from twitter_api.client.twitter_api_mock_client import TwitterApiMockClient
from twitter_api.client.twitter_api_real_client import TwitterApiRealClient


@pytest.fixture
def tweets() -> list[TweetDetail]:
    return [
        TweetDetail(
            id="1460323737035677698",
            text=dedent(
                # flake8: noqa E501
                """
                Introducing a new era for the Twitter Developer Platform! \n
                📣The Twitter API v2 is now the primary API and full of new features
                ⏱Immediate access for most use cases, or apply to get more access for free
                📖Removed certain restrictions in the Policy
                https://t.co/Hrm15bkBWJ https://t.co/YFfCDErHsg
                """
            ).strip(),
            edit_history_tweet_ids=["1460323737035677698"],
        )
    ]


@pytest.mark.skipif(**synthetic_monitoring_is_disable())
class TestGetV2Tweets:
    def test_get_v2_tweets(
        self, real_oauth2_app_client: TwitterApiRealClient, tweets: list[TweetDetail]
    ):
        response = GetV2TweetsResponseBody(data=tweets)
        real_response = (
            real_oauth2_app_client.chain()
            .request("https://api.twitter.com/2/tweets")
            .get({"ids": list(map(lambda tweet: tweet.id, tweets))})
        )

        print(real_response.json())
        print(response.json())

        assert real_response == response


class TestMockGetV2Tweets:
    def test_mock_get_v2_tweets(self, mock_oauth2_app_client: TwitterApiMockClient):
        tweet = TweetDetail(
            id="12345",
            text="tweet",
            edit_history_tweet_ids=["56789"],
        )

        response = GetV2TweetsResponseBody(data=[tweet for _ in range(10)])

        assert (
            mock_oauth2_app_client.chain()
            .inject_get_response_body("https://api.twitter.com/2/tweets", response)
            .request("https://api.twitter.com/2/tweets")
            .get(
                {
                    "ids": "1460323737035677698",
                    "expansions": ["attachments.media_keys"],
                }
            )
        ) == response
