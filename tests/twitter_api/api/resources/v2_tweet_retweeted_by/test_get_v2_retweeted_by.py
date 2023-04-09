import pytest

from tests.conftest import synthetic_monitoring_is_disable
from tests.data import JsonDataLoader
from twitter_api.api.resources.v2_tweet_retweeted_by.get_v2_tweet_retweeted_by import (
    GetV2TweetRetweetedByResponseBody,
)
from twitter_api.client.twitter_api_mock_client import TwitterApiMockClient
from twitter_api.client.twitter_api_real_client import TwitterApiRealClient
from twitter_api.types.extra_permissive_model import get_extra_fields


@pytest.mark.skipif(**synthetic_monitoring_is_disable())
class TestGetV2RetweetedBy:
    def test_get_v2_tweet_retweeted_by(
        self, real_oauth2_app_client: TwitterApiRealClient
    ):
        response = real_oauth2_app_client.request(
            "https://api.twitter.com/2/tweets/:id/retweeted_by"
        ).get("1460323737035677698")

        print(response.json())

        assert get_extra_fields(response) == {}


class TestMockGetV2RetweetedBy:
    def test_mock_get_v2_tweet_retweeted_by(
        self,
        mock_oauth2_app_client: TwitterApiMockClient,
        json_data_loader: JsonDataLoader,
    ):
        response = GetV2TweetRetweetedByResponseBody.parse_obj(
            json_data_loader.load("get_v2_retweeted_by_response.json")
        )

        assert get_extra_fields(response) == {}

        assert (
            mock_oauth2_app_client.chain()
            .inject_get_response_body(
                "https://api.twitter.com/2/tweets/:id/retweeted_by", response
            )
            .request("https://api.twitter.com/2/tweets/:id/retweeted_by")
            .get("1234567890123456789")
        ) == response
