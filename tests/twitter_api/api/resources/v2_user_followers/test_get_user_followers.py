import pytest

from tests.conftest import synthetic_monitoring_is_disable
from tests.contexts.spawn_real_client import spawn_real_client
from tests.data import json_test_data
from twitter_api.api.resources.v2_user_followers.get_v2_user_followers import (
    GetV2UserFollowersResponseBody,
)
from twitter_api.client.twitter_api_async_mock_client import TwitterApiAsyncMockClient
from twitter_api.client.twitter_api_mock_client import TwitterApiMockClient
from twitter_api.types.extra_permissive_model import get_extra_fields


@pytest.mark.skipif(**synthetic_monitoring_is_disable())
class TestGetV2UserFollowers:
    @pytest.mark.parametrize(
        "client_fixture_name,permit",
        [
            ("oauth1_app_real_client", True),
            ("oauth1_user_real_client", True),
            ("oauth2_app_real_client", True),
            ("oauth2_user_real_client", True),
        ],
    )
    def test_get_v2_user_followers(
        self,
        client_fixture_name: str,
        permit: bool,
        request: pytest.FixtureRequest,
    ):
        with spawn_real_client(client_fixture_name, request, permit) as real_client:
            response = (
                real_client.chain()
                .resource("https://api.twitter.com/2/users/:id/followers")
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
        oauth2_app_mock_client: TwitterApiMockClient,
        json_filename: str,
    ):
        response = GetV2UserFollowersResponseBody.parse_file(
            json_test_data(json_filename)
        )

        assert get_extra_fields(response) == {}

        assert (
            oauth2_app_mock_client.chain()
            .inject_get_response_body(
                "https://api.twitter.com/2/users/:id/followers", response
            )
            .resource("https://api.twitter.com/2/users/:id/followers")
            .get("2244994945")
        ) == response


class TestAsyncMockGetV2UserFollowers:
    @pytest.mark.asyncio
    async def test_async_mock_get_v2_user_followers(
        self,
        oauth2_app_async_mock_client: TwitterApiAsyncMockClient,
    ):
        response = GetV2UserFollowersResponseBody.parse_file(
            json_test_data("get_v2_user_followers_response.json")
        )

        assert get_extra_fields(response) == {}

        assert (
            await (
                oauth2_app_async_mock_client.chain()
                .inject_get_response_body(
                    "https://api.twitter.com/2/users/:id/followers", response
                )
                .resource("https://api.twitter.com/2/users/:id/followers")
                .get("2244994945")
            )
            == response
        )
