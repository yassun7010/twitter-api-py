from textwrap import dedent

from twitter_api.client.twitter_api_mock_client import TwitterApiMockClient
from twitter_api.types.oauth1.oauth1_access_token import OAuth1AccessToken


class TestOAuth1AccessToken:
    def test_access_token_jsonify(self):
        assert (
            OAuth1AccessToken(
                oauth_token="oauth_token",
                oauth_token_secret="oauth_token_secret",
                user_id="user_id",
                screen_name="screen_name",
                _client_generator=lambda access_token, access_secret: TwitterApiMockClient.from_oauth1_app_env(),
            ).model_dump_json(indent=4)
            == dedent(
                """
                {
                    "oauth_token": "oauth_token",
                    "oauth_token_secret": "oauth_token_secret",
                    "user_id": "user_id",
                    "screen_name": "screen_name"
                }
                """
            ).strip()
        )
