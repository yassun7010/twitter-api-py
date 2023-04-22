from twitter_api.client.oauth_session.twitter_oauth1_mock_session import (
    TwitterOAuth1MockSession,
)
from twitter_api.types.oauth import AccessSecret, AccessToken


class TwitterOAuth1AsyncMockSession(TwitterOAuth1MockSession):
    def generate_client(self, access_token: AccessToken, access_secret: AccessSecret):
        from twitter_api.client.twitter_api_async_mock_client import (
            TwitterApiAsyncMockClient,
        )

        return TwitterApiAsyncMockClient.from_oauth1_app(
            api_key="api_key",
            api_secret="api_secret",
            access_token=access_token,
            access_secret=access_secret,
        )
