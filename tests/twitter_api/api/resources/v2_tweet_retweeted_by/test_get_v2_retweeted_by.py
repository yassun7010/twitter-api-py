import pytest

from tests.conftest import synthetic_monitoring_is_disable
from tests.contexts.spawn_real_client import spawn_real_client
from tests.data import json_test_data
from twitter_api.api.resources.v2_tweet_retweeted_by.get_v2_tweet_retweeted_by import (
    GetV2TweetRetweetedByResponseBody,
)
from twitter_api.client.twitter_api_async_mock_client import TwitterApiAsyncMockClient
from twitter_api.client.twitter_api_mock_client import TwitterApiMockClient
from twitter_api.types.extra_permissive_model import get_extra_fields


@pytest.mark.skipif(**synthetic_monitoring_is_disable())
class TestGetV2RetweetedBy:
    @pytest.mark.parametrize(
        "client_fixture_name,permit",
        [
            ("oauth1_app_real_client", True),
            ("oauth1_user_real_client", True),
            ("oauth2_app_real_client", True),
            ("oauth2_user_real_client", True),
        ],
    )
    def test_get_v2_tweet_retweeted_by(
        self,
        client_fixture_name: str,
        permit: bool,
        request: pytest.FixtureRequest,
    ):
        with spawn_real_client(client_fixture_name, request, permit) as real_client:
            response_body = real_client.resource(
                "https://api.twitter.com/2/tweets/:id/retweeted_by"
            ).get("1460323737035677698")

            print(response_body.json())

            assert get_extra_fields(response_body) == {}


class TestMockGetV2RetweetedBy:
    def test_mock_get_v2_tweet_retweeted_by(
        self,
        oauth2_app_mock_client: TwitterApiMockClient,
    ):
        response_body = GetV2TweetRetweetedByResponseBody.parse_file(
            json_test_data("get_v2_retweeted_by_response.json")
        )

        assert get_extra_fields(response_body) == {}

        assert (
            oauth2_app_mock_client.chain()
            .inject_get_response_body(
                "https://api.twitter.com/2/tweets/:id/retweeted_by", response_body
            )
            .resource("https://api.twitter.com/2/tweets/:id/retweeted_by")
            .get("1234567890123456789")
        ) == response_body


class TestAsyncMockGetV2RetweetedBy:
    @pytest.mark.asyncio
    async def test_async_mock_get_v2_tweet_retweeted_by(
        self,
        oauth2_app_async_mock_client: TwitterApiAsyncMockClient,
    ):
        response_body = GetV2TweetRetweetedByResponseBody.parse_file(
            json_test_data("get_v2_retweeted_by_response.json")
        )

        assert get_extra_fields(response_body) == {}

        assert (
            await (
                oauth2_app_async_mock_client.chain()
                .inject_get_response_body(
                    "https://api.twitter.com/2/tweets/:id/retweeted_by", response_body
                )
                .resource("https://api.twitter.com/2/tweets/:id/retweeted_by")
                .get("1234567890123456789")
            )
            == response_body
        )
