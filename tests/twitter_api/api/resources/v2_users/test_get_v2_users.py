import pytest

from tests.conftest import synthetic_monitoring_is_disable
from tests.data import JsonDataLoader
from twitter_api.api.resources.v2_users.get_v2_users import GetV2UsersResponseBody
from twitter_api.client.twitter_api_mock_client import TwitterApiMockClient
from twitter_api.client.twitter_api_real_client import TwitterApiRealClient
from twitter_api.types.extra_permissive_model import get_extra_fields


@pytest.mark.skipif(**synthetic_monitoring_is_disable())
class TestGetV2Users:
    def test_get_v2_users(
        self,
        real_oauth2_app_client: TwitterApiRealClient,
    ):
        response = (
            real_oauth2_app_client.chain()
            .request("https://api.twitter.com/2/users")
            .get({"ids": ["2244994945"]})
        )

        print(response.json())

        assert get_extra_fields(response) == {}


class TestMockGetV2Users:
    @pytest.mark.parametrize(
        "json_filename",
        [
            "get_v2_users_response.json",
        ],
    )
    def test_mock_get_v2_users(
        self,
        mock_oauth2_app_client: TwitterApiMockClient,
        json_data_loader: JsonDataLoader,
        json_filename: str,
    ):
        response = GetV2UsersResponseBody.parse_obj(
            json_data_loader.load(json_filename)
        )

        assert get_extra_fields(response) == {}

        assert (
            mock_oauth2_app_client.chain()
            .inject_get_response_body("https://api.twitter.com/2/users", response)
            .request("https://api.twitter.com/2/users")
            .get({"ids": ["2244994945"]})
        ) == response
