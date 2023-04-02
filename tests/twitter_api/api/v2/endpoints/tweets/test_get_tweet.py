from textwrap import dedent

import pytest

from tests.conftest import synthetic_monitoring_is_disable
from twitter_api.api.v2.endpoints.tweets.get_tweet import V2GetTweetResponseBody
from twitter_api.api.v2.types.tweet.tweet import Tweet
from twitter_api.client.twitter_api_mock_client import TwitterApiMockClient
from twitter_api.client.twitter_api_real_client import TwitterApiRealClient


@pytest.fixture
def tweet() -> Tweet:
    return Tweet(
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


@pytest.mark.skipif(**synthetic_monitoring_is_disable())
class TestV2GetTweet:
    def test_get_tweet(
        self, real_app_auth_v2_client: TwitterApiRealClient, tweet: Tweet
    ):
        expected_response = V2GetTweetResponseBody(data=tweet)
        real_response = real_app_auth_v2_client.request(
            "https://api.twitter.com/2/tweets/:id"
        ).get(tweet.id)

        print(real_response.json())
        print(expected_response.json())

        assert real_response == expected_response


class TestMockV2GetTweet:
    def test_mock_get_tweet(
        self, mock_app_auth_v2_client: TwitterApiMockClient, tweet: Tweet
    ):
        expected_response = V2GetTweetResponseBody(data=tweet)

        assert (
            mock_app_auth_v2_client.chain()
            .inject_get_response_body(
                "https://api.twitter.com/2/tweets/:id", expected_response
            )
            .request("https://api.twitter.com/2/tweets/:id")
            .get(tweet.id)
            == expected_response
        )
