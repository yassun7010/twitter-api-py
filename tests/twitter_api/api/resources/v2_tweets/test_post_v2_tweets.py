from datetime import datetime

import pytest

from tests.conftest import synthetic_monitoring_is_disable
from tests.contexts.spawn_real_client import spawn_real_client
from twitter_api.api.resources.v2_tweets.post_v2_tweets import PostV2TweetsResponseBody
from twitter_api.api.types.v2_tweet.tweet import Tweet
from twitter_api.client.twitter_api_mock_client import TwitterApiMockClient


@pytest.mark.skipif(**synthetic_monitoring_is_disable())
class TestGetV2Tweet:
    @pytest.mark.parametrize(
        "client_fixture_name,permit",
        [
            ("oauth1_app_real_client", True),
            ("oauth1_user_real_client", True),
            ("oauth2_app_real_client", False),
            ("oauth2_user_real_client", True),
        ],
    )
    def test_get_v2_tweet(
        self,
        client_fixture_name: str,
        permit: bool,
        request: pytest.FixtureRequest,
    ):
        with spawn_real_client(client_fixture_name, request, permit) as real_client:
            tweet_text = f"テストツイート。{datetime.now().isoformat()}"

            real_response = (
                real_client.chain()
                .resource("https://api.twitter.com/2/tweets")
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
                real_client.chain()
                .resource("https://api.twitter.com/2/tweets/:id")
                .delete(real_response.data.id)
            )

            assert real_response.data.text == tweet_text


class TestMockGetV2Tweet:
    def test_mock_get_v2_tweet(self, oauth2_app_mock_client: TwitterApiMockClient):
        tweet = Tweet(
            id="1234567890123456789",
            text="ツイートしました。",
            edit_history_tweet_ids=["1234567890123456789"],
        )

        response = PostV2TweetsResponseBody(data=tweet)

        assert (
            oauth2_app_mock_client.chain()
            .inject_post_response_body("https://api.twitter.com/2/tweets", response)
            .resource("https://api.twitter.com/2/tweets")
            .post({"text": tweet.text})
        ) == response
