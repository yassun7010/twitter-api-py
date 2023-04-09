import pytest

from tests.conftest import synthetic_monitoring_is_disable
from tests.data import JsonDataLoader
from twitter_api.api.resources.v2_user_tweets.get_v2_user_tweets import (
    GetV2UserTweetsResponseBody,
)
from twitter_api.client.twitter_api_mock_client import TwitterApiMockClient
from twitter_api.client.twitter_api_real_client import TwitterApiRealClient


@pytest.mark.skipif(**synthetic_monitoring_is_disable())
class TestGetV2UserTweets:
    def test_get_v2_user_tweets(
        self,
        real_oauth2_app_client: TwitterApiRealClient,
    ):
        real_response = (
            real_oauth2_app_client.chain()
            .request("https://api.twitter.com/2/users/:id/tweets")
            .get("2244994945")
        )

        print(real_response.json())

        assert True


class TestMockGetV2UserTweets:
    @pytest.mark.parametrize(
        "json_filename",
        [
            "get_user_tweets_response_default_fields.json",
            "get_user_tweets_response_optional_fields.json",
            "get_user_tweets_response_all_fields.json",
        ],
    )
    def test_mock_get_v2_user_tweets(
        self,
        mock_oauth2_app_client: TwitterApiMockClient,
        json_data_loader: JsonDataLoader,
        json_filename: str,
    ):
        expected_response = GetV2UserTweetsResponseBody.parse_obj(
            json_data_loader.load(json_filename)
        )

        assert (
            mock_oauth2_app_client.chain()
            .inject_get_response_body(
                "https://api.twitter.com/2/users/:id/tweets", expected_response
            )
            .request("https://api.twitter.com/2/users/:id/tweets")
            .get("2244994945")
        ) == expected_response
