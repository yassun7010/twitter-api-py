import os

import pytest

from tests.conftest import synthetic_monitoring_is_disable
from twitter_api.api.authentication.endpoints.oauth.post_request_token import (
    OauthPostRequestTokenResponseBody,
)
from twitter_api.client.twitter_api_mock_client import TwitterApiMockClient
from twitter_api.client.twitter_api_real_client import TwitterApiRealClient


@pytest.mark.skipif(**synthetic_monitoring_is_disable())
class TestOauthPostRequestToken:
    def test_post_oauth_request_token(self, real_client: TwitterApiRealClient):
        expected_response = OauthPostRequestTokenResponseBody(
            oauth_token="OAUTH_TOKEN",
            oauth_token_secret="OAUTH_TOKEN_SECRET",
            oauth_callback_confirmed=True,
        )

        real_response = (
            real_client.chain()
            .request("/oauth/request_token")
            .post({"oauth_callback": "https://120.0.0.1:8080"})
        )

        print(real_response.dict())
        print(expected_response.dict())

        assert real_response == expected_response


class TestMockOauthPostRequestToken:
    def test_mock_post_oauth_request_token(self, mock_client: TwitterApiMockClient):
        expected_response = OauthPostRequestTokenResponseBody(
            oauth_token="OAUTH_TOKEN",
            oauth_token_secret="OAUTH_TOKEN_SECRET",
            oauth_callback_confirmed=True,
        )

        assert (
            mock_client.chain()
            .inject_post_response(
                "/oauth/request_token",
                expected_response,
            )
            .request("/oauth/request_token")
            .post({"oauth_callback": "https://120.0.0.1:8080"})
            == expected_response
        )
