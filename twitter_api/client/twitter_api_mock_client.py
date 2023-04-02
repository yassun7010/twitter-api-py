from typing import Optional, Self, overload

from twitter_api.api.authentication.endpoints.oauth import post_request_token
from twitter_api.api.authentication.endpoints.oauth2 import (
    post_invalidate_token,
    post_token,
)
from twitter_api.api.v2.endpoints import tweets
from twitter_api.api.v2.endpoints.tweets.retweeted_by import get_retweeted_by
from twitter_api.api.v2.endpoints.tweets.search.all import get_tweets_search_all
from twitter_api.api.v2.endpoints.tweets.search.recent import get_tweets_search_recent
from twitter_api.rate_limit.manager.rate_limit_manager import RateLimitManager
from twitter_api.rate_limit.rate_limit_target import RateLimitTarget
from twitter_api.types.endpoint import Endpoint
from twitter_api.types.oauth import (
    AccessSecret,
    AccessToken,
    ApiKey,
    ApiSecret,
    OAuthVersion,
)

from .request.mock_request_client import MockRequestClient
from .request.request_client import RequestClient
from .twitter_api_client import TwitterApiClient


class TwitterApiMockClient(TwitterApiClient):
    """Twitter API V2 をモックするためのクライアント"""

    def __init__(
        self,
        *,
        oauth_version: OAuthVersion,
        rate_limit_target: RateLimitTarget,
        rate_limit_manager: Optional[RateLimitManager] = None,
    ) -> None:
        self._client = MockRequestClient(
            oauth_version=oauth_version,
            rate_limit_target=rate_limit_target,
            rate_limit_manager=rate_limit_manager,
        )

    @property
    def _request_client(self) -> RequestClient:
        return self._client

    @overload
    def inject_get_response_body(
        self,
        url: tweets.TweetsUri,
        response: tweets.get_tweets.V2GetTweetsResponseBody,
    ) -> Self:
        ...

    @overload
    def inject_get_response_body(
        self,
        url: tweets.TweetUri,
        response: tweets.get_tweet.V2GetTweetResponseBody,
    ) -> Self:
        ...

    @overload
    def inject_get_response_body(
        self,
        url: get_retweeted_by.Uri,
        response: get_retweeted_by.V2GetRetweetedByResponseBody,
    ) -> Self:
        ...

    @overload
    def inject_get_response_body(
        self,
        url: get_tweets_search_all.Uri,
        response: get_tweets_search_all.V2GetTweetsSearchAllResponseBody,
    ) -> Self:
        ...

    @overload
    def inject_get_response_body(
        self,
        url: get_tweets_search_recent.Uri,
        response: get_tweets_search_recent.V2GetTweetsSearchRecentResponseBody,
    ) -> Self:
        ...

    def inject_get_response_body(self, url, response) -> Self:
        self._client.inject_response_body(Endpoint("GET", url), response)

        return self

    @overload
    def inject_post_response_body(
        self,
        url: post_request_token.Uri,
        response: post_request_token.OauthPostRequestTokenResponseBody,
    ) -> Self:
        ...

    @overload
    def inject_post_response_body(
        self,
        url: post_invalidate_token.Uri,
        response: post_invalidate_token.Oauth2PostInvalidateTokenResponseBody,
    ) -> Self:
        ...

    @overload
    def inject_post_response_body(
        self,
        url: post_token.Uri,
        response: post_token.Oauth2PostTokenResponseBody,
    ) -> Self:
        ...

    @overload
    def inject_post_response_body(
        self,
        url: tweets.TweetsUri,
        response: tweets.post_tweet.V2PostTweetResponseBody,
    ) -> Self:
        ...

    def inject_post_response_body(self, url, response) -> Self:
        self._client.inject_response_body(Endpoint("POST", url), response)

        return self

    def inject_delete_response_body(
        self,
        url: tweets.TweetUri,
        response: tweets.delete_tweet.V2DeleteTweetResponseBody,
    ) -> Self:
        self._client.inject_response_body(Endpoint("DELETE", url), response)

        return self

    @classmethod
    def from_bearer_token(
        cls,
        bearer_token: str,
        *,
        rate_limit_manager: Optional[RateLimitManager] = None,
    ):
        return TwitterApiMockClient(
            oauth_version="2.0",
            rate_limit_target="app",
            rate_limit_manager=rate_limit_manager,
        )

    @classmethod
    def from_app_auth_v2(
        cls,
        *,
        api_key: ApiKey,
        api_secret: ApiSecret,
        rate_limit_manager: Optional[RateLimitManager] = None,
    ) -> Self:
        return TwitterApiMockClient(
            oauth_version="2.0",
            rate_limit_target="app",
            rate_limit_manager=rate_limit_manager,
        )

    @classmethod
    def from_user_auth_v1(
        cls,
        *,
        api_key: ApiKey,
        api_secret: ApiSecret,
        access_token: AccessToken,
        access_secret: AccessSecret,
        rate_limit_manager: Optional[RateLimitManager] = None,
    ):
        return TwitterApiMockClient(
            oauth_version="1.0a",
            rate_limit_target="app",
            rate_limit_manager=rate_limit_manager,
        )
