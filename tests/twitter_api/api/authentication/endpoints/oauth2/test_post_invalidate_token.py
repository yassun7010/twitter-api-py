import os

import pytest

from twitter_api.api.authentication.endpoints.oauth2.post_invalidate_token import (
    PostOauth2InvalidateTokenResponseBody,
)
from twitter_api.client.twitter_api_mock_client import TwitterApiMockClient
from twitter_api.client.twitter_api_real_client import TwitterApiRealClient


class TestOauth2PostInvalidateToken:
    @pytest.mark.skipif(True)
    def test_post_oauth2_invalidate_token(self, real_client: TwitterApiRealClient):
        expected_response = PostOauth2InvalidateTokenResponseBody(
            access_token=(
                real_client._client._auth.token["access_token"]
                # pyright: reportOptionalSubscript=false
                # pyright: reportOptionalMemberAccess=false
            ),
        )

        real_response = (
            real_client.chain()
            .request("/oauth2/invalidate_token")
            .post(
                api_key=os.environ["API_KEY"],
                api_secret=os.environ["API_SECRET"],
                query_parameters={"access_token": expected_response.access_token},
            )
        )

        print(real_response.dict())
        print(expected_response.dict())

        assert real_response == expected_response


class TestMockOauth2PostInvalidateToken:
    def test_mock_post_oauth2_invalidate_token(self, mock_client: TwitterApiMockClient):
        expected_response = PostOauth2InvalidateTokenResponseBody(access_token="")

        assert (
            mock_client.chain()
            .inject_post_response(
                "/oauth2/invalidate_token",
                expected_response,
            )
            .request("/oauth2/invalidate_token")
            .post(
                api_key="DUMMY_API_KEY",
                api_secret="DUMMY_API_SECRET",
                query_parameters={"access_token": "DUMMY_ACCESS_TOKEN"},
            )
            == expected_response
        )
