from datetime import datetime

import pytest

from tests.conftest import synthetic_monitoring_is_disable
from tests.contexts.check_oauth2_user_access_token import check_oauth2_user_access_token
from twitter_api.api.resources.v2_tweets.post_v2_tweets import PostV2TweetsResponseBody
from twitter_api.api.types.v2_tweet.tweet_detail import TweetDetail
from twitter_api.client.twitter_api_mock_client import TwitterApiMockClient
from twitter_api.client.twitter_api_real_client import TwitterApiRealClient


@pytest.mark.skipif(**synthetic_monitoring_is_disable())
class TestGetV2Tweet:
    def test_get_v2_tweet_by_oauth1_user(
        self,
        real_oauth1_user_client: TwitterApiRealClient,
    ):
        tweet_text = f"テストツイート。{datetime.now().isoformat()}"
        real_response = (
            real_oauth1_user_client.chain()
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
            real_oauth1_user_client.chain()
            .request("https://api.twitter.com/2/tweets/:id")
            .delete(real_response.data.id)
        )

        assert real_response.data.text == tweet_text

    def test_get_v2_tweet_by_oauth2_user(
        self,
        real_oauth2_user_client: TwitterApiRealClient,
    ):
        with check_oauth2_user_access_token():
            tweet_text = f"テストツイート。{datetime.now().isoformat()}"
            real_response = (
                real_oauth2_user_client.chain()
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
                real_oauth2_user_client.chain()
                .request("https://api.twitter.com/2/tweets/:id")
                .delete(real_response.data.id)
            )

        assert real_response.data.text == tweet_text


class TestMockGetV2Tweet:
    def test_mock_get_v2_tweet(self, mock_oauth2_app_client: TwitterApiMockClient):
        tweet = TweetDetail(
            id="1234567890123456789",
            text="ツイートしました。",
            edit_history_tweet_ids=["1234567890123456789"],
        )

        response = PostV2TweetsResponseBody(data=tweet)

        assert (
            mock_oauth2_app_client.chain()
            .inject_post_response_body("https://api.twitter.com/2/tweets", response)
            .request("https://api.twitter.com/2/tweets")
            .post({"text": tweet.text})
        ) == response
