import pytest

from tests.conftest import synthetic_monitoring_is_disable
from tests.contexts.spawn_real_client import spawn_real_client
from tests.data import json_test_data
from twitter_api.api.resources.v2_user_retweets.post_v2_user_retweets import (
    PostV2UserRetweetsResponseBody,
)
from twitter_api.client.twitter_api_async_mock_client import TwitterApiAsyncMockClient
from twitter_api.client.twitter_api_mock_client import TwitterApiMockClient
from twitter_api.types.extra_permissive_model import get_extra_fields


@pytest.mark.skipif(**synthetic_monitoring_is_disable())
class TestGetV2UserRetweets:
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
        client_fixture_name: str,
        permit: bool,
        request: pytest.FixtureRequest,
    ):
        with spawn_real_client(client_fixture_name, request, permit) as real_client:
            response_body = (
                real_client.chain()
                .request("https://api.twitter.com/2/users/:id/retweets")
                .post(user_id, {"tweet_id": "1228393702244134912"})
            )

            assert get_extra_fields(response_body) == {}


class TestMockGetV2UserRetweets:
    @pytest.mark.parametrize(
        "json_filename",
        [
            "get_v2_user_retweets_response_body.json",
        ],
    )
    def test_mock_get_v2_user_following(
        self,
        oauth2_app_mock_client: TwitterApiMockClient,
        json_filename: str,
    ):
        response_body = PostV2UserRetweetsResponseBody.parse_file(
            json_test_data(json_filename)
        )

        assert get_extra_fields(response_body) == {}

        assert (
            oauth2_app_mock_client.chain()
            .inject_post_response_body(
                "https://api.twitter.com/2/users/:id/retweets", response_body
            )
            .request("https://api.twitter.com/2/users/:id/retweets")
            .post("2244994945", {"tweet_id": "1228393702244134912"})
        ) == response_body


class TestAsyncMockGetV2UserRetweets:
    @pytest.mark.asyncio
    async def test_async_mock_get_v2_user_following(
        self,
        oauth2_app_async_mock_client: TwitterApiAsyncMockClient,
    ):
        response_body = PostV2UserRetweetsResponseBody.parse_file(
            json_test_data("get_v2_user_retweets_response_body.json")
        )

        assert get_extra_fields(response_body) == {}

        assert (
            await (
                oauth2_app_async_mock_client.chain()
                .inject_post_response_body(
                    "https://api.twitter.com/2/users/:id/retweets", response_body
                )
                .request("https://api.twitter.com/2/users/:id/retweets")
                .post("2244994945", {"tweet_id": "1228393702244134912"})
            )
            == response_body
        )
