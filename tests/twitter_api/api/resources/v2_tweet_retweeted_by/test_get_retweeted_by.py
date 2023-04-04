import pytest

from tests.conftest import synthetic_monitoring_is_disable
from tests.data import JsonDataLoader
from twitter_api.api.resources.v2_tweet_retweeted_by.get_tweet_retweeted_by import (
    V2GetTweetRetweetedByResponseBody,
)
from twitter_api.client.twitter_api_mock_client import TwitterApiMockClient
from twitter_api.client.twitter_api_real_client import TwitterApiRealClient


@pytest.mark.skipif(**synthetic_monitoring_is_disable())
class TestV2GetRetweetedBy:
    def test_get_retweeted_by(self, real_app_auth_v2_client: TwitterApiRealClient):
        real_response = real_app_auth_v2_client.request(
            "https://api.twitter.com/2/tweets/:id/retweeted_by"
        ).get("1460323737035677698")

        print(real_response.json())

        assert True


class TestMockV2GetRetweetedBy:
    def test_mock_get_retweeted_by(
        self,
        mock_app_auth_v2_client: TwitterApiMockClient,
        json_data_loader: JsonDataLoader,
    ):
        expected_response = V2GetTweetRetweetedByResponseBody.parse_obj(
            json_data_loader.load("get_retweeted_by_response.json")
        )

        assert (
            mock_app_auth_v2_client.chain()
            .inject_get_response_body(
                "https://api.twitter.com/2/tweets/:id/retweeted_by", expected_response
            )
            .request("https://api.twitter.com/2/tweets/:id/retweeted_by")
            .get("1234567890123456789")
        ) == expected_response
