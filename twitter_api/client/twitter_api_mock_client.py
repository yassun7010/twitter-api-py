from typing import Self, overload

from twitter_api.api.authentication.endpoints.oauth import post_request_token
from twitter_api.api.authentication.endpoints.oauth2 import (
    post_invalidate_token,
    post_token,
)
from twitter_api.api.v2.endpoints import tweets
from twitter_api.types.endpoint import Endpoint
from twitter_api.types.oauth import (
    AccessSecret,
    AccessToken,
    ApiKey,
    ApiSecret,
    OAuthVersion,
)

from ..utils.ratelimit import RateLimitTarget
from .request.mock_request_client import MockRequestClient
from .request.request_client import RequestClient
from .twitter_api_client import TwitterApiClient


class TwitterApiMockClient(TwitterApiClient):
    """Twitter API V2 をモックするためのクライアント"""

    def __init__(
        self, *, rate_limit: RateLimitTarget, oauth_version: OAuthVersion
    ) -> None:
        self._client = MockRequestClient(
            rate_limit=rate_limit,
            oauth_version=oauth_version,
        )

    @property
    def _request_client(self) -> RequestClient:
        return self._client

    @overload
    def inject_get_response(
        self,
        uri: tweets.TweetsUri,
        response: tweets.get_tweets.V2GetTweetsResponseBody,
    ) -> Self:
        ...

    @overload
    def inject_get_response(
        self,
        uri: tweets.TweetUri,
        response: tweets.get_tweet.V2GetTweetResponseBody,
    ) -> Self:
        ...

    def inject_get_response(self, uri, response) -> Self:
        self._client.inject_response_body(Endpoint("GET", uri), response)

        return self

    @overload
    def inject_post_response(
        self,
        uri: post_request_token.Uri,
        response: post_request_token.OauthPostRequestTokenResponseBody,
    ) -> Self:
        ...

    @overload
    def inject_post_response(
        self,
        uri: post_invalidate_token.Uri,
        response: post_invalidate_token.Oauth2PostInvalidateTokenResponseBody,
    ) -> Self:
        ...

    @overload
    def inject_post_response(
        self,
        uri: post_token.Uri,
        response: post_token.Oauth2PostTokenResponseBody,
    ) -> Self:
        ...

    @overload
    def inject_post_response(
        self,
        uri: tweets.TweetsUri,
        response: tweets.post_tweet.V2PostTweetResponseBody,
    ) -> Self:
        ...

    def inject_post_response(self, uri, response) -> Self:
        self._client.inject_response_body(Endpoint("POST", uri), response)

        return self

    def inject_delete_response(
        self,
        uri: tweets.TweetUri,
        response: tweets.delete_tweet.V2DeleteTweetResponseBody,
    ) -> Self:
        self._client.inject_response_body(Endpoint("DELETE", uri), response)

        return self

    @classmethod
    def from_bearer_token(cls, bearer_token: str):
        return TwitterApiMockClient(
            rate_limit="app",
            oauth_version="2.0",
        )

    @classmethod
    def from_app_auth_v2(
        cls,
        *,
        api_key: ApiKey,
        api_secret: ApiSecret,
    ) -> Self:
        return TwitterApiMockClient(
            rate_limit="app",
            oauth_version="2.0",
        )

    @classmethod
    def from_user_auth_v1(
        cls,
        *,
        api_key: ApiKey,
        api_secret: ApiSecret,
        access_token: AccessToken,
        access_secret: AccessSecret,
    ):
        return TwitterApiMockClient(
            rate_limit="app",
            oauth_version="1.0a",
        )
