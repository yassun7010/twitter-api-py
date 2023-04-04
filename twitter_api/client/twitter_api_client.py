import os
from abc import ABCMeta, abstractmethod
from typing import Optional, Self, Union, overload

from twitter_api.api.authentication.endpoints.oauth import (
    request_token as oauth_request_token,
)
from twitter_api.api.authentication.endpoints.oauth2 import (
    invalidate_token as oauth2_invalidate_token,
)
from twitter_api.api.authentication.endpoints.oauth2 import token as oauth2_token
from twitter_api.api.v2.endpoints import dm_conversations
from twitter_api.api.v2.endpoints import tweets as v2_tweets
from twitter_api.api.v2.endpoints import users as v2_users
from twitter_api.api.v2.endpoints.dm_conversations import with_messages
from twitter_api.api.v2.endpoints.tweets import retweeted_by as v2_tweet_retweeted_by
from twitter_api.api.v2.endpoints.tweets.search import all as v2_tweets_search_all
from twitter_api.api.v2.endpoints.tweets.search import recent as v2_tweets_search_recent
from twitter_api.api.v2.endpoints.tweets.search import stream as v2_tweets_search_stream
from twitter_api.api.v2.endpoints.users import followers as v2_user_followers
from twitter_api.api.v2.endpoints.users import following as v2_user_following
from twitter_api.api.v2.endpoints.users import liked_tweets as v2_user_liked_tweets
from twitter_api.api.v2.endpoints.users import tweets as v2_user_tweets
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
        url: oauth_request_token.OauthRequestTokenUrl,
    ) -> oauth_request_token.OauthRequestTokenResources:
        ...

    @overload
    def request(
        self: Self,
        url: oauth2_token.Oauth2TokenUrl,
    ) -> oauth2_token.Oauth2TokenResources:
        ...

    @overload
    def request(
        self: Self,
        url: oauth2_invalidate_token.Oauth2InvalidateTokenUrl,
    ) -> oauth2_invalidate_token.Oauth2InvalidateTokenResources:
        ...

    @overload
    def request(
        self: Self,
        url: v2_tweets.TweetUrl,
    ) -> v2_tweets.V2TweetResources:
        ...

    @overload
    def request(
        self: Self,
        url: v2_tweets.TweetsUrl,
    ) -> v2_tweets.V2TweetsResources:
        ...

    @overload
    def request(
        self: Self,
        url: v2_tweet_retweeted_by.TweetRetweetedByUrl,
    ) -> v2_tweet_retweeted_by.V2TweetRetweetedByRerources:
        ...

    @overload
    def request(
        self: Self,
        url: v2_tweets_search_all.TweetsSearchAllUrl,
    ) -> v2_tweets_search_all.V2TweetsSearchAllResources:
        ...

    @overload
    def request(
        self: Self,
        url: v2_tweets_search_recent.TweetsSearchRecentUrl,
    ) -> v2_tweets_search_recent.V2GetTweetsSearchRecentResources:
        ...

    @overload
    def request(
        self: Self,
        url: v2_tweets_search_stream.TweetsSearchStreamUrl,
    ) -> v2_tweets_search_stream.V2GetTweetsSearchStreamResources:
        ...

    @overload
    def request(
        self: Self,
        url: v2_users.UsersUrl,
    ) -> v2_users.V2UsersResources:
        ...

    @overload
    def request(
        self: Self,
        url: v2_users.UserUrl,
    ) -> v2_users.V2UserResources:
        ...

    @overload
    def request(
        self: Self,
        url: v2_user_liked_tweets.UserLikedTweetsUrl,
    ) -> v2_user_liked_tweets.V2UserLikedTweetsResources:
        ...

    @overload
    def request(
        self: Self,
        url: v2_user_followers.UserFollowersUrl,
    ) -> v2_user_followers.V2UserFollowersResources:
        ...

    @overload
    def request(
        self: Self,
        url: v2_user_following.UserFollowingUrl,
    ) -> v2_user_following.V2UserFollowingResources:
        ...

    @overload
    def request(
        self: Self,
        url: v2_user_tweets.UserTweetsUrl,
    ) -> v2_user_tweets.V2UserTweetsResources:
        ...

    @overload
    def request(
        self: Self,
        url: with_messages.DmConversationsWithParticipantMessagesUrl,
    ) -> with_messages.V2DmConversationsWithParticipantMessagesResources:
        ...

    @overload
    def request(
        self: Self,
        url: dm_conversations.DmConversationsUrl,
    ) -> dm_conversations.V2DmConversationsResources:
        ...

    def request(
        self: Self,
        url: Union[
            oauth_request_token.OauthRequestTokenUrl,
            oauth2_invalidate_token.Oauth2InvalidateTokenUrl,
            oauth2_token.Oauth2TokenUrl,
            v2_tweet_retweeted_by.TweetRetweetedByUrl,
            v2_tweets_search_all.TweetsSearchAllUrl,
            v2_tweets_search_recent.TweetsSearchRecentUrl,
            v2_tweets_search_stream.TweetsSearchStreamUrl,
            v2_tweets.TweetsUrl,
            v2_tweets.TweetUrl,
            v2_user_followers.UserFollowersUrl,
            v2_user_following.UserFollowingUrl,
            v2_user_liked_tweets.UserLikedTweetsUrl,
            v2_user_tweets.UserTweetsUrl,
            v2_users.UsersUrl,
            v2_users.UserUrl,
            with_messages.DmConversationsWithParticipantMessagesUrl,
            dm_conversations.DmConversationsUrl,
        ],
    ):
        """
        操作したい URI を指定し、実行可能な操作方法を返却します。
        """

        if url == "https://api.twitter.com/oauth/request_token":
            return oauth_request_token.OauthPostRequestToken(
                self._request_client,
            )
        elif url == "https://api.twitter.com/oauth2/token":
            return oauth2_token.Oauth2PostTokenResources(
                self._request_client,
            )
        elif url == "https://api.twitter.com/oauth2/invalidate_token":
            return oauth2_invalidate_token.Oauth2PostInvalidateTokenResources(
                self._request_client,
            )
        elif url == "https://api.twitter.com/2/tweets":
            return v2_tweets.V2TweetsResources(
                self._request_client,
            )
        elif url == "https://api.twitter.com/2/tweets/:id":
            return v2_tweets.V2TweetResources(
                self._request_client,
            )
        elif url == "https://api.twitter.com/2/tweets/:id/retweeted_by":
            return v2_tweet_retweeted_by.V2TweetRetweetedByRerources(
                self._request_client,
            )
        elif url == "https://api.twitter.com/2/tweets/search/all":
            return v2_tweets_search_all.V2TweetsSearchAllResources(
                self._request_client,
            )
        elif url == "https://api.twitter.com/2/tweets/search/recent":
            return v2_tweets_search_recent.V2GetTweetsSearchRecentResources(
                self._request_client,
            )
        elif url == "https://api.twitter.com/2/tweets/search/stream":
            return v2_tweets_search_stream.V2GetTweetsSearchStreamResources(
                self._request_client,
            )
        elif url == "https://api.twitter.com/2/users":
            return v2_users.V2UsersResources(
                self._request_client,
            )
        elif url == "https://api.twitter.com/2/users/:id":
            return v2_users.V2UserResources(
                self._request_client,
            )
        elif url == "https://api.twitter.com/2/users/:id/liked_tweets":
            return v2_user_liked_tweets.V2UserLikedTweetsResources(
                self._request_client,
            )
        elif url == "https://api.twitter.com/2/users/:id/followers":
            return v2_user_followers.V2UserFollowersResources(
                self._request_client,
            )
        elif url == "https://api.twitter.com/2/users/:id/following":
            return v2_user_following.V2UserFollowingResources(
                self._request_client,
            )
        elif url == "https://api.twitter.com/2/users/:id/tweets":
            return v2_user_tweets.V2UserTweetsResources(
                self._request_client,
            )
        elif url == (
            "https://api.twitter.com/2/dm_conversations/with/:participant_id/messages"
        ):
            return with_messages.V2DmConversationsWithParticipantMessagesResources(
                self._request_client,
            )
        elif url == ("https://api.twitter.com/2/dm_conversations"):
            return dm_conversations.V2DmConversationsResources(
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
