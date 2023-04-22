import os

import pytest

from tests.conftest import synthetic_monitoring_is_disable
from twitter_api.api.resources.oauth2_invalidate_token.post_oauth2_invalidate_token import (
    PostOauth2InvalidateTokenResponseBody,
)
from twitter_api.client.twitter_api_async_mock_client import TwitterApiAsyncMockClient
from twitter_api.client.twitter_api_mock_client import TwitterApiMockClient
from twitter_api.client.twitter_api_real_client import TwitterApiRealClient
from twitter_api.types.extra_permissive_model import get_extra_fields


@pytest.mark.skipif(**synthetic_monitoring_is_disable())
class TestPostOauth2InvalidateToken:
    @pytest.mark.xfail(reason="上手く invalidation できない理由を要調査。")
    def test_post_oauth2_invalidate_token(
        self, oauth2_app_real_client: TwitterApiRealClient
    ):
        expected_response = PostOauth2InvalidateTokenResponseBody(
            access_token=os.environ["BEARER_TOEKN"],
        )

        real_response = (
            oauth2_app_real_client.chain()
            .resource("https://api.twitter.com/oauth2/invalidate_token")
            .post(
                api_key=os.environ["API_KEY"],
                api_secret=os.environ["API_SECRET"],
                query={"access_token": expected_response.access_token},
            )
        )

        print(real_response.json())
        print(expected_response.json())

        assert real_response == expected_response
        assert get_extra_fields(expected_response) == {}


class TestMockPostOauth2InvalidateToken:
    def test_mock_post_oauth2_invalidate_token(
        self, oauth2_app_mock_client: TwitterApiMockClient
    ):
        response = PostOauth2InvalidateTokenResponseBody(
            access_token="DUMMY_ACCESS_TOKEN",
        )

        assert get_extra_fields(response) == {}

        assert (
            oauth2_app_mock_client.chain()
            .inject_post_response_body(
                "https://api.twitter.com/oauth2/invalidate_token",
                response,
            )
            .resource("https://api.twitter.com/oauth2/invalidate_token")
            .post(
                api_key="DUMMY_API_KEY",
                api_secret="DUMMY_API_SECRET",
                query={"access_token": "DUMMY_ACCESS_TOKEN"},
            )
        ) == response


class TestAsyncMockPostOauth2InvalidateToken:
    @pytest.mark.asyncio
    async def test_async_mock_post_oauth2_invalidate_token(
        self, oauth2_app_async_mock_client: TwitterApiAsyncMockClient
    ):
        response = PostOauth2InvalidateTokenResponseBody(
            access_token="DUMMY_ACCESS_TOKEN",
        )

        assert get_extra_fields(response) == {}

        assert (
            await (
                oauth2_app_async_mock_client.chain()
                .inject_post_response_body(
                    "https://api.twitter.com/oauth2/invalidate_token",
                    response,
                )
                .resource("https://api.twitter.com/oauth2/invalidate_token")
                .post(
                    api_key="DUMMY_API_KEY",
                    api_secret="DUMMY_API_SECRET",
                    query={"access_token": "DUMMY_ACCESS_TOKEN"},
                )
            )
            == response
        )
