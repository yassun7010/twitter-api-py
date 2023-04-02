from datetime import datetime

import pytest

from tests.conftest import synthetic_monitoring_is_disable
from twitter_api.api.v2.endpoints.tweets.post_tweet import V2PostTweetResponseBody
from twitter_api.api.v2.types.tweet.tweet_detail import TweetDetail
from twitter_api.client.twitter_api_mock_client import TwitterApiMockClient
from twitter_api.client.twitter_api_real_client import TwitterApiRealClient


@pytest.mark.skipif(**synthetic_monitoring_is_disable())
class TestV2GetTweet:
    def test_get_tweet(self, real_user_auth_v1_client: TwitterApiRealClient):
        tweet_text = f"テストツイート。{datetime.now().isoformat()}"
        real_response = (
            real_user_auth_v1_client.chain()
            .request("https://api.twitter.com/2/tweets")
            .post(
                {
                    "text": tweet_text,
                }
            )
        )

        print(real_response.json())
        print(tweet_text)

        assert real_response.data.text == tweet_text


class TestMockV2GetTweet:
    def test_mock_get_tweet(self, mock_app_auth_v2_client: TwitterApiMockClient):
        tweet = TweetDetail(
            id="1234567890123456789",
            text="ツイートしました。",
            edit_history_tweet_ids=["1234567890123456789"],
        )

        expected_response = V2PostTweetResponseBody(data=tweet)

        assert (
            mock_app_auth_v2_client.chain()
            .inject_post_response_body(
                "https://api.twitter.com/2/tweets", expected_response
            )
            .request("https://api.twitter.com/2/tweets")
            .post({"text": tweet.text})
            == expected_response
        )
