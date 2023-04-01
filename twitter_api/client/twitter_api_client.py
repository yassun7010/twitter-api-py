import os
from abc import ABCMeta, abstractmethod
from typing import Self, Union, overload

from twitter_api.api.authentication.endpoints.oauth import post_request_token
from twitter_api.api.authentication.endpoints.oauth2 import (
    post_invalidate_token,
    post_token,
)
from twitter_api.api.v2.endpoints import tweets
from twitter_api.error import NeverError
from twitter_api.types.oauth import AccessSecret, AccessToken, ApiKey, ApiSecret, Env

from .request.request_client import RequestClient


class TwitterApiClient(metaclass=ABCMeta):
    """
    Twitter API を操作するためのクライアント
    """

    @property
    @abstractmethod
    def _request_client(self) -> RequestClient:
        ...

    def chain(self) -> Self:
        """
        メソッドチェーンをキレイに表示させるための関数。
        """

        return self

    @overload
    def request(
        self: Self,
        uri: post_request_token.Uri,
    ) -> post_request_token.OauthPostRequestToken:
        ...

    @overload
    def request(
        self: Self,
        uri: post_token.Uri,
    ) -> post_token.Oauth2PostToken:
        ...

    @overload
    def request(
        self: Self,
        uri: post_invalidate_token.Uri,
    ) -> post_invalidate_token.Oauth2PostInvalidateToken:
        ...

    @overload
    def request(
        self: Self,
        uri: tweets.TweetUri,
    ) -> tweets.V2Tweet:
        ...

    @overload
    def request(
        self: Self,
        uri: tweets.TweetsUri,
    ) -> tweets.V2Tweets:
        ...

    def request(
        self: Self,
        uri: Union[
            tweets.TweetUri,
            tweets.TweetsUri,
            post_request_token.Uri,
            post_invalidate_token.Uri,
            post_token.Uri,
        ],
    ):
        """
        操作したい URI を指定し、実行可能な操作方法を返却します。
        """

        if uri == "/oauth/request_token":
            return post_request_token.OauthPostRequestToken(
                self._request_client,
            )
        elif uri == "/oauth2/token":
            return post_token.Oauth2PostToken(
                self._request_client,
            )
        elif uri == "/oauth2/invalidate_token":
            return post_invalidate_token.Oauth2PostInvalidateToken(
                self._request_client,
            )
        elif uri == "/2/tweets":
            return tweets.V2Tweets(
                self._request_client,
            )
        elif uri == "/2/tweets/:id":
            return tweets.V2Tweet(
                self._request_client,
            )
        else:
            raise NeverError(uri)

    @classmethod
    def from_bearer_token(cls, bearer_token: str) -> Self:
        """Bearer 認証を用いてクライアントを作成する。"""

        from .twitter_api_real_client import TwitterApiRealClient

        return TwitterApiRealClient.from_bearer_token(bearer_token)

    @classmethod
    def from_bearer_token_env(cls, bearer_token="BEARER_TOEKN"):
        """環境変数から、 Bearer 認証を用いてクライアントを作成する。"""

        return cls.from_bearer_token(os.environ[bearer_token])

    @classmethod
    def from_app_auth_v2(
        cls,
        *,
        api_key: ApiKey,
        api_secret: ApiSecret,
    ) -> Self:
        """アプリ認証を用いてクライアントを作成する。"""

        from .twitter_api_real_client import TwitterApiRealClient

        return TwitterApiRealClient.from_app_auth_v2(
            api_key=api_key,
            api_secret=api_secret,
        )

    @classmethod
    def from_app_auth_v2_env(
        cls,
        *,
        api_key: Env[ApiKey] = "API_KEY",
        api_secret: Env[ApiSecret] = "API_SECRET",
    ):
        """環境変数から、アプリ認証を用いてクライアントを作成する。"""

        return cls.from_app_auth_v2(
            api_key=os.environ[api_key],
            api_secret=os.environ[api_secret],
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
        """ユーザ認証を用いてクライアントを作成する。"""

        from .twitter_api_real_client import TwitterApiRealClient

        return TwitterApiRealClient.from_user_auth_v1(
            api_key=api_key,
            api_secret=api_secret,
            access_token=access_token,
            access_secret=access_secret,
        )

    @classmethod
    def from_user_auth_v1_env(
        cls,
        *,
        api_key: Env[ApiKey] = "API_KEY",
        api_secret: Env[ApiSecret] = "API_SECRET",
        access_token: Env[AccessToken] = "ACCESS_TOKEN",
        access_secret: Env[AccessSecret] = "ACCESS_SECRET",
    ):
        """環境変数から、アプリ認証を用いてクライアントを作成する。"""

        return cls.from_user_auth_v1(
            api_key=os.environ[api_key],
            api_secret=os.environ[api_secret],
            access_token=os.environ[access_token],
            access_secret=os.environ[access_secret],
        )
