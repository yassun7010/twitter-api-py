import os
from abc import ABCMeta, abstractmethod
from typing import Optional, Self, Union, overload

import twitter_api.api.v2.endpoints.tweets.retweeted_by as tweet_retweeted_by
import twitter_api.api.v2.endpoints.tweets.search.all as tweets_search_all
import twitter_api.api.v2.endpoints.tweets.search.recent as tweets_search_recent
import twitter_api.api.v2.endpoints.tweets.search.stream as tweets_search_stream
from twitter_api.api.authentication.endpoints.oauth import post_request_token
from twitter_api.api.authentication.endpoints.oauth2 import (
    post_invalidate_token,
    post_token,
)
from twitter_api.api.v2.endpoints import tweets, users
from twitter_api.api.v2.endpoints.users import followers, following, liked_tweets
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
        url: tweet_retweeted_by.TweetRetweetedByUrl,
    ) -> tweet_retweeted_by.V2TweetRetweetedByRerources:
        ...

    @overload
    def request(
        self: Self,
        url: tweets_search_all.TweetsSearchAllUrl,
    ) -> tweets_search_all.V2TweetsSearchAllResources:
        ...

    @overload
    def request(
        self: Self,
        url: tweets_search_recent.TweetsSearchRecentUrl,
    ) -> tweets_search_recent.V2GetTweetsSearchRecentResources:
        ...

    @overload
    def request(
        self: Self,
        url: tweets_search_stream.TweetsSearchStreamUrl,
    ) -> tweets_search_stream.V2GetTweetsSearchStreamResources:
        ...

    @overload
    def request(
        self: Self,
        url: users.UsersUrl,
    ) -> users.V2UsersResources:
        ...

    @overload
    def request(
        self: Self,
        url: users.UserUrl,
    ) -> users.V2UserResources:
        ...

    @overload
    def request(
        self: Self,
        url: liked_tweets.UserLikedTweetsUrl,
    ) -> liked_tweets.V2UserLikedTweetsResources:
        ...

    @overload
    def request(
        self: Self,
        url: followers.UserFollowersUrl,
    ) -> followers.V2UserFollowersResources:
        ...

    @overload
    def request(
        self: Self,
        url: following.UserFollowingUrl,
    ) -> following.V2UserFollowingResources:
        ...

    def request(
        self: Self,
        url: Union[
            tweets.TweetUrl,
            tweets.TweetsUrl,
            post_request_token.Url,
            post_invalidate_token.Url,
            post_token.Url,
            tweet_retweeted_by.TweetRetweetedByUrl,
            tweets_search_all.TweetsSearchAllUrl,
            tweets_search_recent.TweetsSearchRecentUrl,
            tweets_search_stream.TweetsSearchStreamUrl,
            users.UsersUrl,
            users.UserUrl,
            liked_tweets.UserLikedTweetsUrl,
            followers.UserFollowersUrl,
            following.UserFollowingUrl,
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
            return tweet_retweeted_by.V2TweetRetweetedByRerources(
                self._request_client,
            )
        elif url == "https://api.twitter.com/2/tweets/search/all":
            return tweets_search_all.V2TweetsSearchAllResources(
                self._request_client,
            )
        elif url == "https://api.twitter.com/2/tweets/search/recent":
            return tweets_search_recent.V2GetTweetsSearchRecentResources(
                self._request_client,
            )
        elif url == "https://api.twitter.com/2/tweets/search/stream":
            return tweets_search_stream.V2GetTweetsSearchStreamResources(
                self._request_client,
            )
        elif url == "https://api.twitter.com/2/users":
            return users.V2UsersResources(
                self._request_client,
            )
        elif url == "https://api.twitter.com/2/users/:id":
            return users.V2UserResources(
                self._request_client,
            )
        elif url == "https://api.twitter.com/2/users/:id/liked_tweets":
            return liked_tweets.V2UserLikedTweetsResources(
                self._request_client,
            )
        elif url == "https://api.twitter.com/2/users/:id/followers":
            return followers.V2UserFollowersResources(
                self._request_client,
            )
        elif url == "https://api.twitter.com/2/users/:id/following":
            return following.V2UserFollowingResources(
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
            cls._get_env(bearer_token),
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
            api_key=cls._get_env(api_key),
            api_secret=cls._get_env(api_secret),
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
            api_key=cls._get_env(api_key),
            api_secret=cls._get_env(api_secret),
            access_token=cls._get_env(access_token),
            access_secret=cls._get_env(access_secret),
            rate_limit_manager=rate_limit_manager,
        )

    @classmethod
    def _get_env(cls, key: Env[str]) -> str:
        """環境変数を取り出す。"""
        return os.environ[key]
