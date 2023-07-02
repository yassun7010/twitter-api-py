import pytest

from tests.conftest import synthetic_monitoring_is_disable
from tests.contexts.spawn_real_client import spawn_real_client
from tests.data import json_test_data
from twitter_api.client.twitter_api_async_mock_client import TwitterApiAsyncMockClient
from twitter_api.client.twitter_api_mock_client import TwitterApiMockClient
from twitter_api.resources.v2_user_following.post_v2_user_following import (
    PostV2UserFollowingResponseBody,
)
from twitter_api.types.v2_user.user import User


@pytest.mark.skipif(**synthetic_monitoring_is_disable())
class TestGetV2UserFollowing:
    @pytest.mark.parametrize(
        "client_fixture_name,permit",
        [
            ("oauth1_app_real_client", True),
            ("oauth1_user_real_client", True),
            ("oauth2_app_real_client", False),
            ("oauth2_user_real_client", True),
        ],
    )
    def test_get_v2_user_following(
        self,
        user_id,
        twitter_dev_user: User,
        client_fixture_name: str,
        permit: bool,
        request: pytest.FixtureRequest,
    ):
        with spawn_real_client(client_fixture_name, request, permit) as real_client:
            response_body = (
                real_client.chain()
                .request("https://api.twitter.com/2/users/:id/following")
                .post(user_id, {"target_user_id": twitter_dev_user.id})
            )

            assert response_body.model_extra == {}


class TestMockGetV2UserFollowing:
    @pytest.mark.parametrize(
        "json_filename",
        [
            "get_v2_user_following_response_body.json",
        ],
    )
    def test_mock_get_v2_user_following(
        self,
        oauth2_app_mock_client: TwitterApiMockClient,
        twitter_dev_user: User,
        json_filename: str,
    ):
        response_body = PostV2UserFollowingResponseBody.model_validate(
            json_test_data(json_filename)
        )

        assert response_body.model_extra == {}

        assert (
            oauth2_app_mock_client.chain()
            .inject_post_response_body(
                "https://api.twitter.com/2/users/:id/following", response_body
            )
            .request("https://api.twitter.com/2/users/:id/following")
            .post(twitter_dev_user.id, {"target_user_id": twitter_dev_user.id})
        ) == response_body


class TestAsyncMockGetV2UserFollowing:
    @pytest.mark.asyncio
    async def test_async_mock_get_v2_user_following(
        self,
        oauth2_app_async_mock_client: TwitterApiAsyncMockClient,
        twitter_dev_user: User,
    ):
        response_body = PostV2UserFollowingResponseBody.model_validate(
            json_test_data("get_v2_user_following_response_body.json")
        )

        assert response_body.model_extra == {}

        assert (
            await (
                oauth2_app_async_mock_client.chain()
                .inject_post_response_body(
                    "https://api.twitter.com/2/users/:id/following", response_body
                )
                .request("https://api.twitter.com/2/users/:id/following")
                .post(twitter_dev_user.id, {"target_user_id": twitter_dev_user.id})
            )
            == response_body
        )
