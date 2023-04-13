from datetime import datetime

import pytest

from tests.conftest import synthetic_monitoring_is_disable
from tests.contexts.spawn_real_client import spawn_real_client
from twitter_api.api.resources.v2_tweets.post_v2_tweets import PostV2TweetsResponseBody
from twitter_api.api.types.v2_tweet.tweet_detail import TweetDetail
from twitter_api.client.twitter_api_mock_client import TwitterApiMockClient


@pytest.mark.skipif(**synthetic_monitoring_is_disable())
class TestGetV2Tweet:
    @pytest.mark.parametrize(
        "client_fixture_name,permit",
        [
            ("real_oauth1_app_client", True),
            ("real_oauth2_user_client", True),
            ("real_oauth2_app_client", False),
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
                real_client.chain()
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
