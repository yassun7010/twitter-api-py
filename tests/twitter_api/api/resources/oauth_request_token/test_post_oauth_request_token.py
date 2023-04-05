import os

import pytest

from tests.conftest import synthetic_monitoring_is_disable
from twitter_api.client.twitter_api_mock_client import TwitterApiMockClient
from twitter_api.client.twitter_api_real_client import TwitterApiRealClient
from twitter_api.error import TwitterApiOAuthVersionWrong


@pytest.mark.skipif(**synthetic_monitoring_is_disable())
class TestPostOauthRequestToken:
    def test_post_oauth_request_token(
        self, real_app_auth_v2_client: TwitterApiRealClient
    ):
        with pytest.raises(TwitterApiOAuthVersionWrong):
            (
                real_app_auth_v2_client.chain()
                .request("https://api.twitter.com/oauth/request_token")
                .post(
                    api_key=os.environ["API_KEY"],
                    api_secret=os.environ["API_SECRET"],
                    query={"oauth_callback": "https://120.0.0.1:8080"},
                )
            )


class TestMockPostOauthRequestToken:
    def test_mock_post_oauth_request_token(
        self, mock_app_auth_v2_client: TwitterApiMockClient
    ):
        with pytest.raises(TwitterApiOAuthVersionWrong):
            (
                mock_app_auth_v2_client.chain()
                .request("https://api.twitter.com/oauth/request_token")
                .post(
                    api_key="DUMMY_API_KEY",
                    api_secret="DUMMY_API_SECRET",
                    query={"oauth_callback": "https://120.0.0.1:8080"},
                )
            )
