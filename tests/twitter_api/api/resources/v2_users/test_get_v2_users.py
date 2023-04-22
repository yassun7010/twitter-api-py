import pytest

from tests.conftest import synthetic_monitoring_is_disable
from tests.contexts.spawn_real_client import spawn_real_client
from tests.data import json_test_data
from twitter_api.api.resources.v2_users.get_v2_users import GetV2UsersResponseBody
from twitter_api.client.twitter_api_mock_client import TwitterApiMockClient
from twitter_api.types.extra_permissive_model import get_extra_fields


@pytest.mark.skipif(**synthetic_monitoring_is_disable())
class TestGetV2Users:
    @pytest.mark.parametrize(
        "client_fixture_name,permit",
        [
            ("oauth1_app_real_client", True),
            ("oauth1_user_real_client", True),
            ("oauth2_app_real_client", True),
            ("oauth2_user_real_client", True),
        ],
    )
    def test_get_v2_users(
        self,
        client_fixture_name: str,
        permit: bool,
        request: pytest.FixtureRequest,
    ):
        with spawn_real_client(client_fixture_name, request, permit) as real_client:
            response = (
                real_client.chain()
                .resource("https://api.twitter.com/2/users")
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
        oauth2_app_mock_client: TwitterApiMockClient,
        json_filename: str,
    ):
        response = GetV2UsersResponseBody.parse_file(
            json_test_data(json_filename),
        )

        assert get_extra_fields(response) == {}

        assert (
            oauth2_app_mock_client.chain()
            .inject_get_response_body("https://api.twitter.com/2/users", response)
            .resource("https://api.twitter.com/2/users")
            .get({"ids": ["2244994945"]})
        ) == response
