from textwrap import dedent

from twitter_api.client.twitter_api_mock_client import TwitterApiMockClient
from twitter_api.types.oauth2.oauth2_access_token import OAuth2AccessToken


class TestOAuth2AccessToken:
    def test_access_token_jsonify(self):
        assert (
            OAuth2AccessToken(
                token_type="bearer",
                expires_in=0,
                expires_at=0,
                access_token="access_token",
                scope=["tweet.read"],
                _client_generator=lambda access_token: TwitterApiMockClient.from_oauth2_app_env(),
            ).json(indent=4)
            == dedent(
                """
                {
                    "token_type": "bearer",
                    "expires_in": 0,
                    "expires_at": 0,
                    "access_token": "access_token",
                    "scope": [
                        "tweet.read"
                    ]
                }
                """
            ).strip()
        )
