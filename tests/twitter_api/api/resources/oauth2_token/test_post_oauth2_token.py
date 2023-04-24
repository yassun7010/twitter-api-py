import os

import pytest

from tests.conftest import synthetic_monitoring_is_disable
from tests.contexts.spawn_real_client import spawn_real_client
from twitter_api.api.resources.oauth2_token.post_oauth2_token import (
    PostOauth2TokenResponseBody,
)
from twitter_api.client.twitter_api_async_mock_client import TwitterApiAsyncMockClient
from twitter_api.client.twitter_api_mock_client import TwitterApiMockClient
from twitter_api.client.twitter_api_real_client import TwitterApiRealClient
from twitter_api.types.extra_permissive_model import get_extra_fields


@pytest.mark.skipif(**synthetic_monitoring_is_disable())
class TestPostOauth2Token:
    @pytest.mark.parametrize(
        "client_fixture_name,permit",
        [
            ("oauth2_app_real_client", True),
            ("oauth2_user_real_client", True),
        ],
    )
    def test_post_oauth2_token(
        self,
        client_fixture_name: str,
        permit: bool,
        request: pytest.FixtureRequest,
    ):
        with spawn_real_client(client_fixture_name, request, permit) as real_client:
            expected_response = PostOauth2TokenResponseBody(
                token_type="bearer",
                access_token=(
                    real_client._real_request_client._auth.token["access_token"]
                    # pyright: reportOptionalSubscript=false
                    # pyright: reportOptionalMemberAccess=false
                ),
            )

            real_response = (
                real_client.chain()
                .resource("https://api.twitter.com/oauth2/token")
                .post(
                    api_key=os.environ["API_KEY"],
                    api_secret=os.environ["API_SECRET"],
                    query={"grant_type": "client_credentials"},
                )
            )

            print(real_response.json())
            print(expected_response.json())

            assert real_response.token_type == expected_response.token_type
            assert get_extra_fields(real_response) == {}


class TestMockPostOauth2Token:
    def test_mock_post_oauth2_token(self, oauth2_app_mock_client: TwitterApiMockClient):
        response = PostOauth2TokenResponseBody(
            token_type="bearer",
            access_token="AAAAAAAAAAAAAAAAAAAAA",
        )

        assert get_extra_fields(response) == {}

        assert (
            oauth2_app_mock_client.chain()
            .inject_post_response_body(
                "https://api.twitter.com/oauth2/token",
                response,
            )
            .resource("https://api.twitter.com/oauth2/token")
            .post(
                api_key="DUMMY_API_KEY",
                api_secret="DUMMY_API_SECRET",
                query={"grant_type": "client_credentials"},
            )
        ) == response


class TestAsyncMockPostOauth2Token:
    @pytest.mark.asyncio
    async def test_async_mock_post_oauth2_token(
        self, oauth2_app_async_mock_client: TwitterApiAsyncMockClient
    ):
        response = PostOauth2TokenResponseBody(
            token_type="bearer",
            access_token="AAAAAAAAAAAAAAAAAAAAA",
        )

        assert get_extra_fields(response) == {}

        assert (
            await (
                oauth2_app_async_mock_client.chain()
                .inject_post_response_body(
                    "https://api.twitter.com/oauth2/token",
                    response,
                )
                .resource("https://api.twitter.com/oauth2/token")
                .post(
                    api_key="DUMMY_API_KEY",
                    api_secret="DUMMY_API_SECRET",
                    query={"grant_type": "client_credentials"},
                )
            )
            == response
        )
