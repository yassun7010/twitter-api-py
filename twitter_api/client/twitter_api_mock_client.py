from typing import Optional, Self, Type, overload

from twitter_api.api.authentication.endpoints.oauth import post_request_token
from twitter_api.api.authentication.endpoints.oauth2 import (
    post_invalidate_token,
    post_token,
)
from twitter_api.api.v2.endpoints.tweets import get_tweet, get_tweets
from twitter_api.types.endpoint import Endpoint
from twitter_api.types.oauth import (
    AccessSecret,
    AccessToken,
    ApiKey,
    ApiSecret,
    Env,
    OAuthVersion,
)

from .request.mock_request_client import MockRequestClient
from .request.request_client import QuryParameters, RequestClient, ResponseModelBody
from .twitter_api_client import TwitterApiClient


class TwitterApiMockClient(TwitterApiClient):
    """Twitter API V2 をモックするためのクライアント"""

    def __init__(self, *, oauth_version: OAuthVersion = "2.0") -> None:
        self._client = MockRequestClient(oauth_version=oauth_version)

    @property
    def _request_client(self) -> RequestClient:
        return self._client

    @overload
    def inject_get_response(
        self,
        uri: get_tweets.Uri,
        response: get_tweets.V2GetTweetsResponseBody,
    ) -> Self:
        ...

    @overload
    def inject_get_response(
        self,
        uri: get_tweet.Uri,
        response: get_tweet.V2GetTweetResponseBody,
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

    def inject_post_response(self, uri, response) -> Self:
        self._client.inject_response_body(Endpoint("POST", uri), response)

        return self

    @classmethod
    def from_bearer_token_env(cls, bearer_token="BEARER_TOEKN"):
        """環境変数から、 Bearer 認証を用いてクライアントを作成する。"""

        return TwitterApiMockClient(oauth_version="2.0")

    @classmethod
    def from_app_auth_v2(
        cls,
        *,
        api_key: ApiKey,
        api_secret: ApiSecret,
    ) -> Self:
        return TwitterApiMockClient(oauth_version="2.0")

    @classmethod
    def from_app_auth_v2_env(
        cls,
        *,
        api_key: Env[ApiKey] = "API_KEY",
        api_secret: Env[ApiSecret] = "API_SECRET",
    ):
        return TwitterApiMockClient(oauth_version="2.0")

    @classmethod
    def from_user_auth_v1(
        cls,
        *,
        api_key: ApiKey,
        api_secret: ApiSecret,
        access_token: AccessToken,
        access_secret: AccessSecret,
    ):
        return TwitterApiMockClient(oauth_version="1.0a")

    @classmethod
    def from_user_auth_v1_env(
        cls,
        *,
        api_key: Env[ApiKey] = "API_KEY",
        api_secret: Env[ApiSecret] = "API_SECRET",
        access_token: Env[AccessToken] = "ACCESS_TOKEN",
        access_secret: Env[AccessSecret] = "ACCESS_SECRET",
    ):
        return TwitterApiMockClient(oauth_version="1.0a")

    def _get(
        self,
        *,
        endpoint: Endpoint,
        response_type: Type[ResponseModelBody],
        uri: Optional[str] = None,
        query: Optional[QuryParameters] = None,
    ) -> ResponseModelBody:
        return self._client.extract_response_body(endpoint)
