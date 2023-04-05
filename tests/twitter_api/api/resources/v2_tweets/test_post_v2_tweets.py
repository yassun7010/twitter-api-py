from datetime import datetime

import pytest

from tests.conftest import synthetic_monitoring_is_disable
from twitter_api.api.resources.v2_tweets.post_v2_tweets import PostV2TweetsResponseBody
from twitter_api.api.types.v2_tweet.tweet_detail import TweetDetail
from twitter_api.client.twitter_api_mock_client import TwitterApiMockClient
from twitter_api.client.twitter_api_real_client import TwitterApiRealClient


@pytest.mark.skipif(**synthetic_monitoring_is_disable())
class TestGetV2Tweet:
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

        # テストが終わったらデータを消しておく。
        (
            real_user_auth_v1_client.chain()
            .request("https://api.twitter.com/2/tweets/:id")
            .delete(real_response.data.id)
        )

        assert real_response.data.text == tweet_text


class TestMockGetV2Tweet:
    def test_mock_get_tweet(self, mock_app_auth_v2_client: TwitterApiMockClient):
        tweet = TweetDetail(
            id="1234567890123456789",
            text="ツイートしました。",
            edit_history_tweet_ids=["1234567890123456789"],
        )

        expected_response = PostV2TweetsResponseBody(data=tweet)

        assert (
            mock_app_auth_v2_client.chain()
            .inject_post_response_body(
                "https://api.twitter.com/2/tweets", expected_response
            )
            .request("https://api.twitter.com/2/tweets")
            .post({"text": tweet.text})
        ) == expected_response
