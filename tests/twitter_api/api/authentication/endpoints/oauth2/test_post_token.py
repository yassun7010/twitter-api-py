import os

import pytest

from tests.conftest import synthetic_monitoring_is_disable
from twitter_api.api.authentication.endpoints.oauth2.post_token import (
    Oauth2PostTokenResponseBody,
)
from twitter_api.client.twitter_api_mock_client import TwitterApiMockClient
from twitter_api.client.twitter_api_real_client import TwitterApiRealClient


@pytest.mark.skipif(**synthetic_monitoring_is_disable())
class TestOauth2PostToken:
    def test_post_oauth2_token(self, real_client: TwitterApiRealClient):
        expected_response = Oauth2PostTokenResponseBody(
            token_type="bearer",
            access_token=(
                real_client._client._auth.token["access_token"]
                # pyright: reportOptionalSubscript=false
                # pyright: reportOptionalMemberAccess=false
            ),
        )

        real_response = (
            real_client.chain()
            .request("/oauth2/token")
            .post(
                api_key=os.environ["API_KEY"],
                api_secret=os.environ["API_SECRET"],
                query_parameters={"grant_type": "client_credentials"},
            )
        )

        print(real_response.dict())
        print(expected_response.dict())

        assert real_response == expected_response


class TestMockOauth2PostToken:
    def test_mock_post_oauth2_token(self, mock_client: TwitterApiMockClient):
        expected_response = Oauth2PostTokenResponseBody(
            token_type="bearer",
            access_token="AAAAAAAAAAAAAAAAAAAAAOeOmQEAAAAAu",
        )

        assert (
            mock_client.chain()
            .inject_post_response(
                "/oauth2/token",
                expected_response,
            )
            .request("/oauth2/token")
            .post(
                api_key="DUMMY_API_KEY",
                api_secret="DUMMY_API_SECRET",
                query_parameters={"grant_type": "client_credentials"},
            )
            == expected_response
        )
