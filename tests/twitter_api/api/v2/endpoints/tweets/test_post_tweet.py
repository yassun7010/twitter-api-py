from datetime import datetime

import pytest

from tests.conftest import synthetic_monitoring_is_disable
from twitter_api.api.v2.endpoints.tweets.get_tweet import V2GetTweetResponseBody
from twitter_api.api.v2.endpoints.tweets.post_tweet import V2PostTweetResponseBody
from twitter_api.api.v2.types.tweet.tweet import Tweet
from twitter_api.client.twitter_api_mock_client import TwitterApiMockClient
from twitter_api.client.twitter_api_real_client import TwitterApiRealClient


@pytest.fixture
def tweet() -> Tweet:
    return Tweet(
        id="1234567890123456789",
        text="ツイートしました。",
        edit_history_tweet_ids=["1234567890123456789"],
    )


@pytest.mark.skipif(**synthetic_monitoring_is_disable())
class TestV2GetTweet:
    def test_get_tweet(
        self, real_app_auth_v2_client: TwitterApiRealClient, tweet: Tweet
    ):
        expected_response = V2GetTweetResponseBody(data=tweet)
        real_response = (
            real_app_auth_v2_client.chain()
            .request("/2/tweets")
            .post({"text": f"テストツイート。{datetime.now().isoformat()}"})
        )

        print(real_response.dict())
        print(expected_response.dict())

        assert real_response == expected_response


class TestMockV2GetTweet:
    def test_mock_get_tweet(
        self, mock_app_auth_v2_client: TwitterApiMockClient, tweet: Tweet
    ):
        expected_response = V2PostTweetResponseBody(data=tweet)

        assert (
            mock_app_auth_v2_client.chain()
            .inject_post_response("/2/tweets", expected_response)
            .request("/2/tweets")
            .post({"text": tweet.text})
            == expected_response
        )
