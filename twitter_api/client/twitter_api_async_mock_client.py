from typing import Optional, Self

from twitter_api.api.types.v2_scope import Scope
from twitter_api.client.twitter_api_async_client import TwitterApiAsyncClient
from twitter_api.client.twitter_api_mock_client import TwitterApiMockClient
from twitter_api.rate_limit.manager.rate_limit_manager import RateLimitManager
from twitter_api.types.oauth import (
    AccessSecret,
    AccessToken,
    ApiKey,
    ApiSecret,
    CallbackUrl,
    ClientId,
    ClientSecret,
)


class TwitterApiAsyncMockClient(TwitterApiMockClient, TwitterApiAsyncClient):
    @classmethod
    def from_oauth2_bearer_token(
        cls,
        bearer_token: str,
        *,
        rate_limit_manager: Optional[RateLimitManager] = None,
    ):
        return TwitterApiAsyncMockClient(
            oauth_version="2.0",
            rate_limit_target="app",
            rate_limit_manager=rate_limit_manager,
        )

    @classmethod
    def from_oauth2_app(
        cls,
        *,
        api_key: ApiKey,
        api_secret: ApiSecret,
        rate_limit_manager: Optional[RateLimitManager] = None,
    ) -> Self:
        return TwitterApiAsyncMockClient(
            oauth_version="2.0",
            rate_limit_target="app",
            rate_limit_manager=rate_limit_manager,
        )

    @classmethod
    def from_oauth2_user_flow(
        cls,
        *,
        client_id: ClientId,
        client_secret: ClientSecret,
        callback_url: CallbackUrl,
        scope: list[Scope],
        rate_limit_manager: Optional[RateLimitManager] = None,
    ):
        from twitter_api.client.oauth_flow.twitter_oauth2_authorization_client import (
            TwitterOAuth2AuthorizeClient,
        )
        from twitter_api.client.oauth_session.twitter_oauth2_async_mock_session import (
            TwitterOAuth2AsyncMockSession,
        )

        session = TwitterOAuth2AsyncMockSession(scope=scope)
        return TwitterOAuth2AuthorizeClient(session=session)

    @classmethod
    def from_oauth1_app(
        cls,
        *,
        api_key: ApiKey,
        api_secret: ApiSecret,
        access_token: AccessToken,
        access_secret: AccessSecret,
        rate_limit_manager: Optional[RateLimitManager] = None,
    ):
        return TwitterApiAsyncMockClient(
            oauth_version="1.0a",
            rate_limit_target="app",
            rate_limit_manager=rate_limit_manager,
        )

    @classmethod
    def from_oauth1_user_flow(
        cls,
        *,
        api_key: ApiKey,
        api_secret: ApiSecret,
        callback_url: CallbackUrl,
        rate_limit_manager: Optional[RateLimitManager] = None,
    ):
        from twitter_api.client.oauth_flow.twitter_oauth1_request_token_client import (
            TwitterOAuth1RequestTokenClient,
        )
        from twitter_api.client.oauth_session.twitter_oauth1_async_mock_session import (
            TwitterOAuth1AsyncMockSession,
        )

        session = TwitterOAuth1AsyncMockSession()
        return TwitterOAuth1RequestTokenClient(session=session)
