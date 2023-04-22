from twitter_api.client.oauth_session.twitter_oauth2_mock_session import (
    TwitterOAuth2MockSession,
)


class TwitterOAuth2AsyncMockSession(TwitterOAuth2MockSession):
    def generate_client(self, access_token: str):
        from twitter_api.client.twitter_api_async_mock_client import (
            TwitterApiAsyncMockClient,
        )

        return TwitterApiAsyncMockClient.from_oauth2_bearer_token(
            bearer_token=access_token
        )
