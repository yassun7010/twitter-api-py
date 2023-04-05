import os
from abc import ABCMeta, abstractmethod
from typing import Optional, Self, Union, overload

from twitter_api.api.resources.oauth2_invalidate_token import (
    Oauth2InvalidateTokenResources,
    Oauth2InvalidateTokenUrl,
)
from twitter_api.api.resources.oauth2_token import Oauth2TokenResources, Oauth2TokenUrl
from twitter_api.api.resources.oauth_request_token import (
    OauthRequestTokenResources,
    OauthRequestTokenUrl,
)
from twitter_api.api.resources.v2_dm_conversation_messages import (
    V2DmConversationMessagesResources,
    V2DmConversationsMessagesUrl,
)
from twitter_api.api.resources.v2_dm_conversations import (
    V2DmConversationsResources,
    V2DmConversationsUrl,
)
from twitter_api.api.resources.v2_dm_conversations_with_messages import (
    V2DmConversationsWithParticipantMessagesResources,
    V2DmConversationsWithParticipantMessagesUrl,
)
from twitter_api.api.resources.v2_tweet import V2TweetResources, V2TweetUrl
from twitter_api.api.resources.v2_tweet_retweeted_by import (
    V2TweetRetweetedByRerources,
    V2TweetRetweetedByUrl,
)
from twitter_api.api.resources.v2_tweets import V2TweetsResources, V2TweetsUrl
from twitter_api.api.resources.v2_tweets_search_all import (
    V2TweetsSearchAllResources,
    V2TweetsSearchAllUrl,
)
from twitter_api.api.resources.v2_tweets_search_recent import V2TweetsSearchRecentUrl
from twitter_api.api.resources.v2_tweets_search_recent.get_v2_tweets_search_recent import (
    GetV2TweetsSearchRecentResources,
)
from twitter_api.api.resources.v2_tweets_search_stream import V2TweetsSearchStreamUrl
from twitter_api.api.resources.v2_tweets_search_stream.get_v2_tweets_search_stream import (
    GetV2TweetsSearchStreamResources,
)
from twitter_api.api.resources.v2_user import V2UserResources, V2UserUrl
from twitter_api.api.resources.v2_user_followers import (
    V2UserFollowersResources,
    V2UserFollowersUrl,
)
from twitter_api.api.resources.v2_user_following import (
    V2UserFollowingResources,
    V2UserFollowingUrl,
)
from twitter_api.api.resources.v2_user_liked_tweets import (
    V2UserLikedTweetsResources,
    V2UserLikedTweetsUrl,
)
from twitter_api.api.resources.v2_user_retweets import (
    V2UserRetweetsResources,
    V2UserRetweetsUrl,
)
from twitter_api.api.resources.v2_user_tweets import (
    V2UserTweetsResources,
    V2UserTweetsUrl,
)
from twitter_api.api.resources.v2_users import V2UsersResources, V2UsersUrl
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
        url: OauthRequestTokenUrl,
    ) -> OauthRequestTokenResources:
        ...

    @overload
    def request(
        self: Self,
        url: Oauth2TokenUrl,
    ) -> Oauth2TokenResources:
        ...

    @overload
    def request(
        self: Self,
        url: Oauth2InvalidateTokenUrl,
    ) -> Oauth2InvalidateTokenResources:
        ...

    @overload
    def request(
        self: Self,
        url: V2TweetUrl,
    ) -> V2TweetResources:
        ...

    @overload
    def request(
        self: Self,
        url: V2TweetsUrl,
    ) -> V2TweetsResources:
        ...

    @overload
    def request(
        self: Self,
        url: V2TweetRetweetedByUrl,
    ) -> V2TweetRetweetedByRerources:
        ...

    @overload
    def request(
        self: Self,
        url: V2TweetsSearchAllUrl,
    ) -> V2TweetsSearchAllResources:
        ...

    @overload
    def request(
        self: Self,
        url: V2TweetsSearchRecentUrl,
    ) -> GetV2TweetsSearchRecentResources:
        ...

    @overload
    def request(
        self: Self,
        url: V2TweetsSearchStreamUrl,
    ) -> GetV2TweetsSearchStreamResources:
        ...

    @overload
    def request(
        self: Self,
        url: V2UsersUrl,
    ) -> V2UsersResources:
        ...

    @overload
    def request(
        self: Self,
        url: V2UserUrl,
    ) -> V2UserResources:
        ...

    @overload
    def request(
        self: Self,
        url: V2UserLikedTweetsUrl,
    ) -> V2UserLikedTweetsResources:
        ...

    @overload
    def request(
        self: Self,
        url: V2UserFollowersUrl,
    ) -> V2UserFollowersResources:
        ...

    @overload
    def request(
        self: Self,
        url: V2UserFollowingUrl,
    ) -> V2UserFollowingResources:
        ...

    @overload
    def request(
        self: Self,
        url: V2UserRetweetsUrl,
    ) -> V2UserRetweetsResources:
        ...

    @overload
    def request(
        self: Self,
        url: V2UserTweetsUrl,
    ) -> V2UserTweetsResources:
        ...

    @overload
    def request(
        self: Self,
        url: V2DmConversationsWithParticipantMessagesUrl,
    ) -> V2DmConversationsWithParticipantMessagesResources:
        ...

    @overload
    def request(
        self: Self,
        url: V2DmConversationsUrl,
    ) -> V2DmConversationsResources:
        ...

    @overload
    def request(
        self: Self,
        url: V2DmConversationsMessagesUrl,
    ) -> V2DmConversationMessagesResources:
        ...

    def request(
        self: Self,
        url: Union[
            OauthRequestTokenUrl,
            Oauth2InvalidateTokenUrl,
            Oauth2TokenUrl,
            V2TweetRetweetedByUrl,
            V2TweetsSearchAllUrl,
            V2TweetsSearchRecentUrl,
            V2TweetsSearchStreamUrl,
            V2TweetsUrl,
            V2TweetUrl,
            V2UserFollowersUrl,
            V2UserFollowingUrl,
            V2UserRetweetsUrl,
            V2UserLikedTweetsUrl,
            V2UserTweetsUrl,
            V2UsersUrl,
            V2UserUrl,
            V2DmConversationsWithParticipantMessagesUrl,
            V2DmConversationsUrl,
            V2DmConversationsMessagesUrl,
        ],
    ):
        """
        操作したい URI を指定し、実行可能な操作方法を返却します。
        """

        if url == "https://api.twitter.com/oauth/request_token":
            return OauthRequestTokenResources(
                self._request_client,
            )
        elif url == "https://api.twitter.com/oauth2/token":
            return Oauth2TokenResources(
                self._request_client,
            )
        elif url == "https://api.twitter.com/oauth2/invalidate_token":
            return Oauth2InvalidateTokenResources(
                self._request_client,
            )
        elif url == "https://api.twitter.com/2/tweets":
            return V2TweetsResources(
                self._request_client,
            )
        elif url == "https://api.twitter.com/2/tweets/:id":
            return V2TweetResources(
                self._request_client,
            )
        elif url == "https://api.twitter.com/2/tweets/:id/retweeted_by":
            return V2TweetRetweetedByRerources(
                self._request_client,
            )
        elif url == "https://api.twitter.com/2/tweets/search/all":
            return V2TweetsSearchAllResources(
                self._request_client,
            )
        elif url == "https://api.twitter.com/2/tweets/search/recent":
            return GetV2TweetsSearchRecentResources(
                self._request_client,
            )
        elif url == "https://api.twitter.com/2/tweets/search/stream":
            return GetV2TweetsSearchStreamResources(
                self._request_client,
            )
        elif url == "https://api.twitter.com/2/users":
            return V2UsersResources(
                self._request_client,
            )
        elif url == "https://api.twitter.com/2/users/:id":
            return V2UserResources(
                self._request_client,
            )
        elif url == "https://api.twitter.com/2/users/:id/liked_tweets":
            return V2UserLikedTweetsResources(
                self._request_client,
            )
        elif url == "https://api.twitter.com/2/users/:id/followers":
            return V2UserFollowersResources(
                self._request_client,
            )
        elif url == "https://api.twitter.com/2/users/:id/following":
            return V2UserFollowingResources(
                self._request_client,
            )
        elif url == "https://api.twitter.com/2/users/:id/retweets":
            return V2UserRetweetsResources(
                self._request_client,
            )
        elif url == "https://api.twitter.com/2/users/:id/tweets":
            return V2UserTweetsResources(
                self._request_client,
            )
        elif (
            url
            == "https://api.twitter.com/2/dm_conversations/with/:participant_id/messages"
        ):
            return V2DmConversationsWithParticipantMessagesResources(
                self._request_client,
            )
        elif url == ("https://api.twitter.com/2/dm_conversations"):
            return V2DmConversationsResources(
                self._request_client,
            )
        elif url == (
            "https://api.twitter.com/2/dm_conversations/:dm_conversation_id/messages"
        ):
            return V2DmConversationMessagesResources(
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
