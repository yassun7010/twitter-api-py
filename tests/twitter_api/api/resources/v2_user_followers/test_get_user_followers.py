import pytest

from tests.conftest import synthetic_monitoring_is_disable
from tests.data import JsonDataLoader
from twitter_api.api.resources.v2_user_followers.get_v2_user_followers import (
    GetV2UserFollowersResponseBody,
)
from twitter_api.client.twitter_api_mock_client import TwitterApiMockClient
from twitter_api.client.twitter_api_real_client import TwitterApiRealClient
from twitter_api.types.extra_permissive_model import get_extra_fields


@pytest.mark.skipif(**synthetic_monitoring_is_disable())
class TestGetV2UserFollowers:
    def test_get_v2_user_followers(
        self,
        real_oauth2_app_client: TwitterApiRealClient,
    ):
        response = (
            real_oauth2_app_client.chain()
            .request("https://api.twitter.com/2/users/:id/followers")
            .get("2244994945")
        )

        print(response.json())

        assert get_extra_fields(response) == {}


class TestMockGetV2UserFollowers:
    @pytest.mark.parametrize(
        "json_filename",
        [
            "get_v2_user_followers_response.json",
        ],
    )
    def test_mock_get_v2_user_followers(
        self,
        mock_oauth2_app_client: TwitterApiMockClient,
        json_data_loader: JsonDataLoader,
        json_filename: str,
    ):
        response = GetV2UserFollowersResponseBody.parse_obj(
            json_data_loader.load(json_filename)
        )

        assert get_extra_fields(response) == {}

        assert (
            mock_oauth2_app_client.chain()
            .inject_get_response_body(
                "https://api.twitter.com/2/users/:id/followers", response
            )
            .request("https://api.twitter.com/2/users/:id/followers")
            .get("2244994945")
        ) == response
