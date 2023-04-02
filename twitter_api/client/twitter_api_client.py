import os
from abc import ABCMeta, abstractmethod
from typing import Optional, Self, Union, overload

from twitter_api.api.authentication.endpoints.oauth import post_request_token
from twitter_api.api.authentication.endpoints.oauth2 import (
    post_invalidate_token,
    post_token,
)
from twitter_api.api.v2.endpoints import tweets, users
from twitter_api.api.v2.endpoints.tweets.retweeted_by import get_retweeted_by
from twitter_api.api.v2.endpoints.tweets.search.all import get_tweets_search_all
from twitter_api.api.v2.endpoints.tweets.search.recent import get_tweets_search_recent
from twitter_api.api.v2.endpoints.tweets.search.stream import get_tweets_search_stream
from twitter_api.api.v2.endpoints.users import followers, liked_tweets
from twitter_api.error import NeverError
from twitter_api.rate_limit.manager.rate_limit_manager import RateLimitManager
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

        あくまで black というフォーマッタを用いてコードを書くとき、
        キレイな見た目にするために使う。ロジック的な意味はない。
        """

        return self

    @overload
    def request(
        self: Self,
        url: post_request_token.Url,
    ) -> post_request_token.OauthPostRequestToken:
        ...

    @overload
    def request(
        self: Self,
        url: post_token.Url,
    ) -> post_token.Oauth2PostToken:
        ...

    @overload
    def request(
        self: Self,
        url: post_invalidate_token.Url,
    ) -> post_invalidate_token.Oauth2PostInvalidateToken:
        ...

    @overload
    def request(
        self: Self,
        url: tweets.TweetUrl,
    ) -> tweets.V2Tweet:
        ...

    @overload
    def request(
        self: Self,
        url: tweets.TweetsUrl,
    ) -> tweets.V2Tweets:
        ...

    @overload
    def request(
        self: Self,
        url: get_retweeted_by.Url,
    ) -> get_retweeted_by.V2GetRetweetedBy:
        ...

    @overload
    def request(
        self: Self,
        url: get_tweets_search_all.Url,
    ) -> get_tweets_search_all.V2GetTweetsSearchAll:
        ...

    @overload
    def request(
        self: Self,
        url: get_tweets_search_recent.Url,
    ) -> get_tweets_search_recent.V2GetTweetsSearchRecent:
        ...

    @overload
    def request(
        self: Self,
        url: get_tweets_search_stream.Url,
    ) -> get_tweets_search_stream.V2GetTweetsSearchStream:
        ...

    @overload
    def request(
        self: Self,
        url: users.UsersUrl,
    ) -> users.V2Users:
        ...

    @overload
    def request(
        self: Self,
        url: users.UserUrl,
    ) -> users.V2User:
        ...

    @overload
    def request(
        self: Self,
        url: liked_tweets.UserLikedTweetsUrl,
    ) -> liked_tweets.V2UserLikedTweets:
        ...

    @overload
    def request(
        self: Self,
        url: followers.UserFollowersUrl,
    ) -> followers.V2UserFollowers:
        ...

    def request(
        self: Self,
        url: Union[
            tweets.TweetUrl,
            tweets.TweetsUrl,
            post_request_token.Url,
            post_invalidate_token.Url,
            post_token.Url,
            get_retweeted_by.Url,
            get_tweets_search_all.Url,
            get_tweets_search_recent.Url,
            get_tweets_search_stream.Url,
            users.UsersUrl,
            users.UserUrl,
            liked_tweets.UserLikedTweetsUrl,
            followers.UserFollowersUrl,
        ],
    ):
        """
        操作したい URI を指定し、実行可能な操作方法を返却します。
        """

        if url == "https://api.twitter.com/oauth/request_token":
            return post_request_token.OauthPostRequestToken(
                self._request_client,
            )
        elif url == "https://api.twitter.com/oauth2/token":
            return post_token.Oauth2PostToken(
                self._request_client,
            )
        elif url == "https://api.twitter.com/oauth2/invalidate_token":
            return post_invalidate_token.Oauth2PostInvalidateToken(
                self._request_client,
            )
        elif url == "https://api.twitter.com/2/tweets":
            return tweets.V2Tweets(
                self._request_client,
            )
        elif url == "https://api.twitter.com/2/tweets/:id":
            return tweets.V2Tweet(
                self._request_client,
            )
        elif url == "https://api.twitter.com/2/tweets/:id/retweeted_by":
            return get_retweeted_by.V2GetRetweetedBy(
                self._request_client,
            )
        elif url == "https://api.twitter.com/2/tweets/search/all":
            return get_tweets_search_all.V2GetTweetsSearchAll(
                self._request_client,
            )
        elif url == "https://api.twitter.com/2/tweets/search/recent":
            return get_tweets_search_recent.V2GetTweetsSearchRecent(
                self._request_client,
            )
        elif url == "https://api.twitter.com/2/tweets/search/stream":
            return get_tweets_search_stream.V2GetTweetsSearchStream(
                self._request_client,
            )
        elif url == "https://api.twitter.com/2/users":
            return users.V2Users(
                self._request_client,
            )
        elif url == "https://api.twitter.com/2/users/:id":
            return users.V2User(
                self._request_client,
            )
        elif url == "https://api.twitter.com/2/users/:id/liked_tweets":
            return liked_tweets.V2UserLikedTweets(
                self._request_client,
            )
        elif url == "https://api.twitter.com/2/users/:id/followers":
            return followers.V2UserFollowers(
                self._request_client,
            )
        else:
            raise NeverError(url)

    @classmethod
    def from_bearer_token(
        cls,
        bearer_token: str,
        *,
        rate_limit_manager: Optional[RateLimitManager] = None,
    ) -> Self:
        """Bearer 認証を用いてクライアントを作成する。"""

        from .twitter_api_real_client import TwitterApiRealClient

        return TwitterApiRealClient.from_bearer_token(
            bearer_token,
            rate_limit_manager=rate_limit_manager,
        )

    @classmethod
    def from_bearer_token_env(
        cls,
        bearer_token="BEARER_TOEKN",
        rate_limit_manager: Optional[RateLimitManager] = None,
    ):
        """環境変数から、 Bearer 認証を用いてクライアントを作成する。"""

        return cls.from_bearer_token(
            os.environ[bearer_token],
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
        """アプリ認証を用いてクライアントを作成する。"""

        from .twitter_api_real_client import TwitterApiRealClient

        return TwitterApiRealClient.from_app_auth_v2(
            api_key=api_key,
            api_secret=api_secret,
            rate_limit_manager=rate_limit_manager,
        )

    @classmethod
    def from_app_auth_v2_env(
        cls,
        *,
        api_key: Env[ApiKey] = "API_KEY",
        api_secret: Env[ApiSecret] = "API_SECRET",
        rate_limit_manager: Optional[RateLimitManager] = None,
    ):
        """環境変数から、アプリ認証を用いてクライアントを作成する。"""

        return cls.from_app_auth_v2(
            api_key=os.environ[api_key],
            api_secret=os.environ[api_secret],
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
        """ユーザ認証を用いてクライアントを作成する。"""

        from .twitter_api_real_client import TwitterApiRealClient

        return TwitterApiRealClient.from_user_auth_v1(
            api_key=api_key,
            api_secret=api_secret,
            access_token=access_token,
            access_secret=access_secret,
            rate_limit_manager=rate_limit_manager,
        )

    @classmethod
    def from_user_auth_v1_env(
        cls,
        *,
        api_key: Env[ApiKey] = "API_KEY",
        api_secret: Env[ApiSecret] = "API_SECRET",
        access_token: Env[AccessToken] = "ACCESS_TOKEN",
        access_secret: Env[AccessSecret] = "ACCESS_SECRET",
        rate_limit_manager: Optional[RateLimitManager] = None,
    ):
        """環境変数から、アプリ認証を用いてクライアントを作成する。"""

        return cls.from_user_auth_v1(
            api_key=os.environ[api_key],
            api_secret=os.environ[api_secret],
            access_token=os.environ[access_token],
            access_secret=os.environ[access_secret],
            rate_limit_manager=rate_limit_manager,
        )
