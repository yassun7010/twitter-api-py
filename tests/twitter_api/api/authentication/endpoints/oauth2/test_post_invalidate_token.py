import os

import pytest

from tests.conftest import synthetic_monitoring_is_disable
from twitter_api.api.authentication.endpoints.oauth2.post_invalidate_token import (
    Oauth2PostInvalidateTokenResponseBody,
)
from twitter_api.client.twitter_api_mock_client import TwitterApiMockClient
from twitter_api.client.twitter_api_real_client import TwitterApiRealClient


@pytest.mark.skipif(**synthetic_monitoring_is_disable())
class TestOauth2PostInvalidateToken:
    @pytest.mark.skipif(True, reason="上手く invalidation できない理由を要調査。")
    def test_post_oauth2_invalidate_token(
        self, real_app_auth_v2_client: TwitterApiRealClient
    ):
        expected_response = Oauth2PostInvalidateTokenResponseBody(
            access_token=(
                real_app_auth_v2_client._client._auth.token["access_token"]
                # pyright: reportOptionalSubscript=false
                # pyright: reportOptionalMemberAccess=false
            ),
        )

        real_response = (
            real_app_auth_v2_client.chain()
            .request("https://api.twitter.com/oauth2/invalidate_token")
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
    def test_mock_post_oauth2_invalidate_token(
        self, mock_app_auth_v2_client: TwitterApiMockClient
    ):
        expected_response = Oauth2PostInvalidateTokenResponseBody(access_token="")

        assert (
            mock_app_auth_v2_client.chain()
            .inject_post_response(
                "https://api.twitter.com/oauth2/invalidate_token",
                expected_response,
            )
            .request("https://api.twitter.com/oauth2/invalidate_token")
            .post(
                api_key="DUMMY_API_KEY",
                api_secret="DUMMY_API_SECRET",
                query_parameters={"access_token": "DUMMY_ACCESS_TOKEN"},
            )
            == expected_response
        )
