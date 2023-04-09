from textwrap import dedent

import pytest

from tests.conftest import synthetic_monitoring_is_disable
from twitter_api.api.resources.v2_tweet.get_v2_tweet import GetV2TweetResponseBody
from twitter_api.api.types.v2_tweet.tweet_detail import TweetDetail
from twitter_api.client.twitter_api_mock_client import TwitterApiMockClient
from twitter_api.client.twitter_api_real_client import TwitterApiRealClient


@pytest.fixture
def tweet() -> TweetDetail:
    return TweetDetail(
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
class TestGetV2Tweet:
    def test_get_v2_tweet(
        self, real_oauth2_app_client: TwitterApiRealClient, tweet: TweetDetail
    ):
        expected_response = GetV2TweetResponseBody(data=tweet)
        real_response = real_oauth2_app_client.request(
            "https://api.twitter.com/2/tweets/:id"
        ).get(tweet.id)

        print(real_response.json())
        print(expected_response.json())

        assert real_response == expected_response


class TestMockGetV2Tweet:
    def test_mock_get_v2_tweet(
        self, mock_oauth2_app_client: TwitterApiMockClient, tweet: TweetDetail
    ):
        expected_response = GetV2TweetResponseBody(data=tweet)

        assert (
            mock_oauth2_app_client.chain()
            .inject_get_response_body(
                "https://api.twitter.com/2/tweets/:id", expected_response
            )
            .request("https://api.twitter.com/2/tweets/:id")
            .get(tweet.id)
        ) == expected_response
