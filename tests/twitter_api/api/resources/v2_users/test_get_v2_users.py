import pytest

from tests.conftest import synthetic_monitoring_is_disable
from tests.data import JsonDataLoader
from twitter_api.api.resources.v2_users.get_v2_users import GetV2UsersResponseBody
from twitter_api.client.twitter_api_mock_client import TwitterApiMockClient
from twitter_api.client.twitter_api_real_client import TwitterApiRealClient


@pytest.mark.skipif(**synthetic_monitoring_is_disable())
class TestGetV2Users:
    def test_get_v2_users(
        self,
        real_app_auth_v2_client: TwitterApiRealClient,
    ):
        real_response = (
            real_app_auth_v2_client.chain()
            .request("https://api.twitter.com/2/users")
            .get({"ids": ["2244994945"]})
        )

        print(real_response.json())

        assert True


class TestMockGetV2Users:
    @pytest.mark.parametrize(
        "json_filename",
        [
            "get_users_response.json",
        ],
    )
    def test_mock_get_v2_users(
        self,
        mock_app_auth_v2_client: TwitterApiMockClient,
        json_data_loader: JsonDataLoader,
        json_filename: str,
    ):
        expected_response = GetV2UsersResponseBody.parse_obj(
            json_data_loader.load(json_filename)
        )

        assert (
            mock_app_auth_v2_client.chain()
            .inject_get_response_body(
                "https://api.twitter.com/2/users", expected_response
            )
            .request("https://api.twitter.com/2/users")
            .get({"ids": ["2244994945"]})
        ) == expected_response