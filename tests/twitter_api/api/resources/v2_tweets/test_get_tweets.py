from textwrap import dedent

import pytest

from tests.conftest import synthetic_monitoring_is_disable
from twitter_api.api.resources.v2_tweets.get_tweets import V2GetTweetsResponseBody
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
class TestV2GetTweets:
    def test_get_tweets(
        self, real_app_auth_v2_client: TwitterApiRealClient, tweets: list[TweetDetail]
    ):
        expected_response = V2GetTweetsResponseBody(data=tweets)
        real_response = (
            real_app_auth_v2_client.chain()
            .request("https://api.twitter.com/2/tweets")
            .get({"ids": list(map(lambda tweet: tweet.id, tweets))})
        )

        print(real_response.json())
        print(expected_response.json())

        assert real_response == expected_response


class TestMockV2GetTweets:
    def test_mock_get_tweets(self, mock_app_auth_v2_client: TwitterApiMockClient):
        tweet = TweetDetail(
            id="12345",
            text="tweet",
            edit_history_tweet_ids=["56789"],
        )

        response = V2GetTweetsResponseBody(data=[tweet for _ in range(10)])

        assert (
            mock_app_auth_v2_client.chain()
            .inject_get_response_body("https://api.twitter.com/2/tweets", response)
            .request("https://api.twitter.com/2/tweets")
            .get(
                {"ids": "1460323737035677698", "expansions": ["attachments.media_keys"]}
            )
            == response
        )
