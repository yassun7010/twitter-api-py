import os
from abc import abstractmethod
from typing import Optional, Self, Union, overload

from twitter_api.api.resources.oauth2_invalidate_token import (
    AsyncOauth2InvalidateTokenResources,
    Oauth2InvalidateTokenUrl,
)
from twitter_api.api.resources.oauth2_token import (
    AsyncOauth2TokenResources,
    Oauth2TokenUrl,
)
from twitter_api.api.resources.v2_dm_conversation_messages import (
    AsyncV2DmConversationMessagesResources,
    V2DmConversationsMessagesUrl,
)
from twitter_api.api.resources.v2_dm_conversations import (
    AsyncV2DmConversationsResources,
    V2DmConversationsUrl,
)
from twitter_api.api.resources.v2_dm_conversations_with_messages import (
    AsyncV2DmConversationsWithParticipantMessagesResources,
    V2DmConversationsWithParticipantMessagesUrl,
)
from twitter_api.api.resources.v2_tweet import AsyncV2TweetResources, V2TweetUrl
from twitter_api.api.resources.v2_tweet_retweeted_by import (
    AsyncV2TweetRetweetedByRerources,
    V2TweetRetweetedByUrl,
)
from twitter_api.api.resources.v2_tweets import AsyncV2TweetsResources, V2TweetsUrl
from twitter_api.api.resources.v2_tweets_search_all import (
    AsyncV2TweetsSearchAllResources,
    V2TweetsSearchAllUrl,
)
from twitter_api.api.resources.v2_tweets_search_recent import (
    AsyncV2TweetsSearchRecentResources,
    V2TweetsSearchRecentUrl,
)
from twitter_api.api.resources.v2_tweets_search_stream import (
    AsyncV2TweetsSearchStreamResources,
    V2TweetsSearchStreamUrl,
)
from twitter_api.api.resources.v2_tweets_search_stream_rules import (
    AsyncV2TweetsSearchStreamRulesResources,
    V2TweetsSearchStreamRulesUrl,
)
from twitter_api.api.resources.v2_user import AsyncV2UserResources, V2UserUrl
from twitter_api.api.resources.v2_user_followers import (
    AsyncV2UserFollowersResources,
    V2UserFollowersUrl,
)
from twitter_api.api.resources.v2_user_following import (
    AsyncV2UserFollowingResources,
    V2UserFollowingUrl,
)
from twitter_api.api.resources.v2_user_liked_tweets import (
    AsyncV2UserLikedTweetsResources,
    V2UserLikedTweetsUrl,
)
from twitter_api.api.resources.v2_user_retweets import (
    AsyncV2UserRetweetsResources,
    V2UserRetweetsUrl,
)
from twitter_api.api.resources.v2_user_tweets import (
    AsyncV2UserTweetsResources,
    V2UserTweetsUrl,
)
from twitter_api.api.resources.v2_users import AsyncV2UsersResources, V2UsersUrl
from twitter_api.api.types.v2_scope import ALL_SCOPES, Scope
from twitter_api.client.request.request_async_client import RequestAsyncClient
from twitter_api.client.twitter_api_client import TwitterApiClient
from twitter_api.error import NeverError
from twitter_api.rate_limit.manager.rate_limit_manager import RateLimitManager
from twitter_api.types.oauth import (
    AccessSecret,
    AccessToken,
    ApiKey,
    ApiSecret,
    CallbackUrl,
    ClientId,
    ClientSecret,
    Env,
)


class TwitterApiAsyncClient(TwitterApiClient):
    """
    Twitter API を非同期に操作するためのクライアント
    """

    @property
    @abstractmethod
    def _request_client(self) -> RequestAsyncClient:
        ...

    @overload
    def resource(
        self: Self,
        url: Oauth2TokenUrl,
    ) -> AsyncOauth2TokenResources:
        ...

    @overload
    def resource(
        self: Self,
        url: Oauth2InvalidateTokenUrl,
    ) -> AsyncOauth2InvalidateTokenResources:
        ...

    @overload
    def resource(
        self: Self,
        url: V2TweetUrl,
    ) -> AsyncV2TweetResources:
        ...

    @overload
    def resource(
        self: Self,
        url: V2TweetsUrl,
    ) -> AsyncV2TweetsResources:
        ...

    @overload
    def resource(
        self: Self,
        url: V2TweetRetweetedByUrl,
    ) -> AsyncV2TweetRetweetedByRerources:
        ...

    @overload
    def resource(
        self: Self,
        url: V2TweetsSearchAllUrl,
    ) -> AsyncV2TweetsSearchAllResources:
        ...

    @overload
    def resource(
        self: Self,
        url: V2TweetsSearchRecentUrl,
    ) -> AsyncV2TweetsSearchRecentResources:
        ...

    @overload
    def resource(
        self: Self,
        url: V2TweetsSearchStreamUrl,
    ) -> AsyncV2TweetsSearchStreamResources:
        ...

    @overload
    def resource(
        self: Self,
        url: V2TweetsSearchStreamRulesUrl,
    ) -> AsyncV2TweetsSearchStreamRulesResources:
        ...

    @overload
    def resource(
        self: Self,
        url: V2UsersUrl,
    ) -> AsyncV2UsersResources:
        ...

    @overload
    def resource(
        self: Self,
        url: V2UserUrl,
    ) -> AsyncV2UserResources:
        ...

    @overload
    def resource(
        self: Self,
        url: V2UserLikedTweetsUrl,
    ) -> AsyncV2UserLikedTweetsResources:
        ...

    @overload
    def resource(
        self: Self,
        url: V2UserFollowersUrl,
    ) -> AsyncV2UserFollowersResources:
        ...

    @overload
    def resource(
        self: Self,
        url: V2UserFollowingUrl,
    ) -> AsyncV2UserFollowingResources:
        ...

    @overload
    def resource(
        self: Self,
        url: V2UserRetweetsUrl,
    ) -> AsyncV2UserRetweetsResources:
        ...

    @overload
    def resource(
        self: Self,
        url: V2UserTweetsUrl,
    ) -> AsyncV2UserTweetsResources:
        ...

    @overload
    def resource(
        self: Self,
        url: V2DmConversationsWithParticipantMessagesUrl,
    ) -> AsyncV2DmConversationsWithParticipantMessagesResources:
        ...

    @overload
    def resource(
        self: Self,
        url: V2DmConversationsUrl,
    ) -> AsyncV2DmConversationsResources:
        ...

    @overload
    def resource(
        self: Self,
        url: V2DmConversationsMessagesUrl,
    ) -> AsyncV2DmConversationMessagesResources:
        ...

    def resource(
        self: Self,
        url: Union[
            Oauth2InvalidateTokenUrl,
            Oauth2TokenUrl,
            V2TweetRetweetedByUrl,
            V2TweetsSearchAllUrl,
            V2TweetsSearchRecentUrl,
            V2TweetsSearchStreamUrl,
            V2TweetsSearchStreamRulesUrl,
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

        if url == "https://api.twitter.com/oauth2/token":
            return AsyncOauth2TokenResources(
                self._request_client,
            )
        elif url == "https://api.twitter.com/oauth2/invalidate_token":
            return AsyncOauth2InvalidateTokenResources(
                self._request_client,
            )
        elif url == "https://api.twitter.com/2/tweets":
            return AsyncV2TweetsResources(
                self._request_client,
            )
        elif url == "https://api.twitter.com/2/tweets/:id":
            return AsyncV2TweetResources(
                self._request_client,
            )
        elif url == "https://api.twitter.com/2/tweets/:id/retweeted_by":
            return AsyncV2TweetRetweetedByRerources(
                self._request_client,
            )
        elif url == "https://api.twitter.com/2/tweets/search/all":
            return AsyncV2TweetsSearchAllResources(
                self._request_client,
            )
        elif url == "https://api.twitter.com/2/tweets/search/recent":
            return AsyncV2TweetsSearchRecentResources(
                self._request_client,
            )
        elif url == "https://api.twitter.com/2/tweets/search/stream":
            return AsyncV2TweetsSearchStreamResources(
                self._request_client,
            )
        elif url == "https://api.twitter.com/2/tweets/search/stream/rules":
            return AsyncV2TweetsSearchStreamRulesResources(
                self._request_client,
            )
        elif url == "https://api.twitter.com/2/users":
            return AsyncV2UsersResources(
                self._request_client,
            )
        elif url == "https://api.twitter.com/2/users/:id":
            return AsyncV2UserResources(
                self._request_client,
            )
        elif url == "https://api.twitter.com/2/users/:id/liked_tweets":
            return AsyncV2UserLikedTweetsResources(
                self._request_client,
            )
        elif url == "https://api.twitter.com/2/users/:id/followers":
            return AsyncV2UserFollowersResources(
                self._request_client,
            )
        elif url == "https://api.twitter.com/2/users/:id/following":
            return AsyncV2UserFollowingResources(
                self._request_client,
            )
        elif url == "https://api.twitter.com/2/users/:id/retweets":
            return AsyncV2UserRetweetsResources(
                self._request_client,
            )
        elif url == "https://api.twitter.com/2/users/:id/tweets":
            return AsyncV2UserTweetsResources(
                self._request_client,
            )
        elif (
            url
            == "https://api.twitter.com/2/dm_conversations/with/:participant_id/messages"
        ):
            return AsyncV2DmConversationsWithParticipantMessagesResources(
                self._request_client,
            )
        elif url == ("https://api.twitter.com/2/dm_conversations"):
            return AsyncV2DmConversationsResources(
                self._request_client,
            )
        elif url == (
            "https://api.twitter.com/2/dm_conversations/:dm_conversation_id/messages"
        ):
            return AsyncV2DmConversationMessagesResources(
                self._request_client,
            )
        else:
            raise NeverError(url)

    @classmethod
    def from_oauth2_bearer_token(
        cls,
        bearer_token: str,
        *,
        rate_limit_manager: Optional[RateLimitManager] = None,
    ) -> Self:
        """OAuth 2.0 の Bearer 認証を用いてクライアントを作成する。"""

        from twitter_api.client.twitter_api_async_real_client import (
            TwitterApiAsyncRealClient,
        )

        return TwitterApiAsyncRealClient.from_oauth2_bearer_token(
            bearer_token,
            rate_limit_manager=rate_limit_manager,
        )

    @classmethod
    def from_oauth2_bearer_token_env(
        cls,
        bearer_token_env="BEARER_TOEKN",
        rate_limit_manager: Optional[RateLimitManager] = None,
    ) -> Self:
        """環境変数から、 OAuth 2.0 の Bearer 認証を用いてクライアントを作成する。"""

        return cls.from_oauth2_bearer_token(
            cls._get_env(bearer_token_env),
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
        """OAuth 2.0 のアプリ認証を用いてクライアントを作成する。"""

        from twitter_api.client.twitter_api_async_real_client import (
            TwitterApiAsyncRealClient,
        )

        return TwitterApiAsyncRealClient.from_oauth2_app(
            api_key=api_key,
            api_secret=api_secret,
            rate_limit_manager=rate_limit_manager,
        )

    @classmethod
    def from_oauth2_app_env(
        cls,
        *,
        api_key_env: Env[ApiKey] = "API_KEY",
        api_secret_env: Env[ApiSecret] = "API_SECRET",
        rate_limit_manager: Optional[RateLimitManager] = None,
    ) -> Self:
        """環境変数から、OAuth 2.0 のアプリ認証を用いてクライアントを作成する。"""

        return cls.from_oauth2_app(
            api_key=cls._get_env(api_key_env),
            api_secret=cls._get_env(api_secret_env),
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
    ):
        """
        OAuth 2.0 のユーザ認証を用いてクライアントを作成する。
        """

        from .twitter_api_real_client import TwitterApiRealClient

        return TwitterApiRealClient.from_oauth2_user_flow(
            client_id=client_id,
            client_secret=client_secret,
            scope=scope,
            callback_url=callback_url,
        )

    @classmethod
    def from_oauth2_user_flow_env(
        cls,
        *,
        scope: Optional[list[Scope]] = None,
        client_id_env: Env[ClientId] = "CLIENT_ID",
        client_secret_env: Env[ClientSecret] = "CLIENT_SECRET",
        callback_url_env: Env[CallbackUrl] = "CALLBACK_URL",
        callback_url: Optional[CallbackUrl] = None,
    ):
        """
        環境変数から、 OAuth 2.0 のユーザ認証を用いてクライアントを作成する。

        refer: https://developer.twitter.com/en/docs/authentication/oauth-2-0/authorization-code
        """

        if scope is None:
            scope = ALL_SCOPES

        return cls.from_oauth2_user_flow(
            client_id=cls._get_env(client_id_env),
            client_secret=cls._get_env(client_secret_env),
            scope=scope,
            callback_url=(
                callback_url
                if callback_url is not None
                else cls._get_env(callback_url_env)
            ),
        )

    @classmethod
    def from_oauth1_app(
        cls,
        *,
        api_key: ApiKey,
        api_secret: ApiSecret,
        access_token: AccessToken,
        access_secret: AccessSecret,
        rate_limit_manager: Optional[RateLimitManager] = None,
    ) -> Self:
        """OAuth1.0a のアプリ認証を用いてクライアントを作成する。"""

        from twitter_api.client.twitter_api_async_real_client import (
            TwitterApiAsyncRealClient,
        )

        return TwitterApiAsyncRealClient.from_oauth1_app(
            api_key=api_key,
            api_secret=api_secret,
            access_token=access_token,
            access_secret=access_secret,
            rate_limit_manager=rate_limit_manager,
        )

    @classmethod
    def from_oauth1_app_env(
        cls,
        *,
        api_key_env: Env[ApiKey] = "API_KEY",
        api_secret_env: Env[ApiSecret] = "API_SECRET",
        access_token_env: Env[AccessToken] = "ACCESS_TOKEN",
        access_secret_env: Env[AccessSecret] = "ACCESS_SECRET",
        rate_limit_manager: Optional[RateLimitManager] = None,
    ) -> Self:
        """環境変数から、OAuth1.0a のアプリ認証を用いてクライアントを作成する。"""

        return cls.from_oauth1_app(
            api_key=cls._get_env(api_key_env),
            api_secret=cls._get_env(api_secret_env),
            access_token=cls._get_env(access_token_env),
            access_secret=cls._get_env(access_secret_env),
            rate_limit_manager=rate_limit_manager,
        )

    @classmethod
    def from_oauth1_user_flow(
        cls,
        *,
        api_key: ApiKey,
        api_secret: ApiSecret,
        callback_url: CallbackUrl,
    ):
        """
        OAuth 1.0a のユーザ認証を用いてクライアントを作成する。
        """

        from .twitter_api_real_client import TwitterApiRealClient

        return TwitterApiRealClient.from_oauth1_user_flow(
            api_key=api_key,
            api_secret=api_secret,
            callback_url=callback_url,
        )

    @classmethod
    def from_oauth1_user_flow_env(
        cls,
        *,
        api_key_env: Env[ApiKey] = "API_KEY",
        api_secret_env: Env[ApiSecret] = "API_SECRET",
        callback_url_env: Env[CallbackUrl] = "CALLBACK_URL",
        callback_url: Optional[CallbackUrl] = None,
    ):
        """
        環境変数から、 OAuth 1.0a のユーザ認証を用いてクライアントを作成する。

        refer: https://developer.twitter.com/en/docs/authentication/oauth-1-0a/obtaining-user-access-tokens
        """

        return cls.from_oauth1_user_flow(
            api_key=cls._get_env(api_key_env),
            api_secret=cls._get_env(api_secret_env),
            callback_url=(
                callback_url
                if callback_url is not None
                else cls._get_env(callback_url_env)
            ),
        )

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(self, exc_type, exc_value, traceback) -> None:
        pass

    @classmethod
    def _get_env(cls, key: Env[str]) -> str:
        """環境変数を取り出す。"""
        return os.environ[key]
