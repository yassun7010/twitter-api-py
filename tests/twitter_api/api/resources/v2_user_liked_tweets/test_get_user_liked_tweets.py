import pytest

from tests.conftest import synthetic_monitoring_is_disable
from tests.data import JsonDataLoader
from twitter_api.api.resources.v2_user_liked_tweets.get_user_liked_tweets import (
    V2GetUserLikedTweetsResponseBody,
)
from twitter_api.client.twitter_api_mock_client import TwitterApiMockClient
from twitter_api.client.twitter_api_real_client import TwitterApiRealClient


@pytest.mark.skipif(**synthetic_monitoring_is_disable())
class TestV2GetUserLikedTweets:
    def test_get_user_liked_tweets(
        self,
        real_app_auth_v2_client: TwitterApiRealClient,
    ):
        real_response = (
            real_app_auth_v2_client.chain()
            .request("https://api.twitter.com/2/users/:id/liked_tweets")
            .get("2244994945")
        )

        print(real_response.json())

        assert True


class TestMockV2GetUserLikedTweets:
    @pytest.mark.parametrize(
        "json_filename",
        [
            "get_user_liked_tweets_response.json",
        ],
    )
    def test_mock_get_user_liked_tweets(
        self,
        mock_app_auth_v2_client: TwitterApiMockClient,
        json_data_loader: JsonDataLoader,
        json_filename: str,
    ):
        expected_response = V2GetUserLikedTweetsResponseBody.parse_obj(
            json_data_loader.load(json_filename)
        )

        assert (
            mock_app_auth_v2_client.chain()
            .inject_get_response_body(
                "https://api.twitter.com/2/users/:id/liked_tweets", expected_response
            )
            .request("https://api.twitter.com/2/users/:id/liked_tweets")
            .get("2244994945")
        ) == expected_response
