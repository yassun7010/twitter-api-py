from abc import ABCMeta, abstractmethod
from typing import Self, Union, overload

from twitter_api.api.authentication.endpoints.oauth import post_request_token
from twitter_api.api.authentication.endpoints.oauth2 import (
    post_invalidate_token,
    post_token,
)
from twitter_api.api.v2.endpoints.tweets import get_tweet, get_tweets
from twitter_api.error import NeverError
from twitter_api.types.oauth import (
    AccessSecret,
    AccessToken,
    ConsumerKey,
    ConsumerSecret,
    Env,
)

from .request.request_client import RequestClient


class TwitterApiClient(metaclass=ABCMeta):
    """Twitter API V2 を操作するためのクライアント"""

    @property
    @abstractmethod
    def _request_client(self) -> RequestClient:
        ...

    def chain(self) -> Self:
        """メソッドチェーンをキレイに表示させるための関数。"""

        return self

    @overload
    def request(
        self: Self,
        uri: post_request_token.Uri,
    ) -> post_request_token.PostOauthRequestToken:
        ...

    @overload
    def request(
        self: Self,
        uri: post_token.Uri,
    ) -> post_token.PostOauth2Token:
        ...

    @overload
    def request(
        self: Self,
        uri: post_invalidate_token.Uri,
    ) -> post_invalidate_token.PostOauth2InvalidateToken:
        ...

    @overload
    def request(
        self: Self,
        uri: get_tweets.Uri,
    ) -> get_tweets.GetTweets:
        ...

    @overload
    def request(
        self: Self,
        uri: get_tweet.Uri,
    ) -> get_tweet.GetTweet:
        ...

    def request(
        self: Self,
        uri: Union[
            get_tweet.Uri,
            get_tweets.Uri,
            post_request_token.Uri,
            post_invalidate_token.Uri,
            post_token.Uri,
        ],
    ):
        if uri == "/oauth/request_token":
            return post_request_token.PostOauthRequestToken(
                self._request_client,
            )
        elif uri == "/oauth2/token":
            return post_token.PostOauth2Token(
                self._request_client,
            )
        elif uri == "/oauth2/invalidate_token":
            return post_invalidate_token.PostOauth2InvalidateToken(
                self._request_client,
            )
        elif uri == "/2/tweets":
            return get_tweets.GetTweets(
                self._request_client,
            )
        elif uri == "/2/tweets/:id":
            return get_tweet.GetTweet(
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

        from .twitter_api_real_client import TwitterApiRealClient

        return TwitterApiRealClient.from_bearer_token_env(bearer_token)

    @classmethod
    def from_app_auth(
        cls,
        *,
        consumer_key: ConsumerKey,
        consumer_secret: ConsumerSecret,
    ) -> Self:
        """アプリ認証を用いてクライアントを作成する。"""

        from .twitter_api_real_client import TwitterApiRealClient

        return TwitterApiRealClient.from_app_auth(
            consumer_key=consumer_key,
            consumer_secret=consumer_secret,
        )

    @classmethod
    def from_app_auth_env(
        cls,
        *,
        consumer_key: Env[ConsumerKey] = "CONSUMER_KEY",
        consumer_secret: Env[ConsumerSecret] = "CONSUMER_SECRET",
    ):
        """環境変数から、アプリ認証を用いてクライアントを作成する。"""

        from .twitter_api_real_client import TwitterApiRealClient

        return TwitterApiRealClient.from_app_auth_env(
            consumer_key=consumer_key,
            consumer_secret=consumer_secret,
        )

    @classmethod
    def from_user_auth(
        cls,
        *,
        consumer_key: ConsumerKey,
        consumer_secret: ConsumerSecret,
        access_token: AccessToken,
        access_secret: AccessSecret,
    ):
        """ユーザ認証を用いてクライアントを作成する。"""

        from .twitter_api_real_client import TwitterApiRealClient

        return TwitterApiRealClient.from_user_auth(
            consumer_key=consumer_key,
            consumer_secret=consumer_secret,
            access_token=access_token,
            access_secret=access_secret,
        )

    @classmethod
    def from_user_auth_env(
        cls,
        *,
        consumer_key: Env[ConsumerKey] = "CONSUMER_KEY",
        consumer_secret: Env[ConsumerSecret] = "CONSUMER_SECRET",
        access_token: Env[AccessToken] = "ACCESS_TOKEN",
        access_secret: Env[AccessSecret] = "ACCESS_SECRET",
    ):
        """環境変数から、アプリ認証を用いてクライアントを作成する。"""

        from .twitter_api_real_client import TwitterApiRealClient

        return TwitterApiRealClient.from_user_auth_env(
            consumer_key=consumer_key,
            consumer_secret=consumer_secret,
            access_token=access_token,
            access_secret=access_secret,
        )
