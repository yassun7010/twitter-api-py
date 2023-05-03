import os
from abc import ABCMeta, abstractmethod
from typing import Mapping, Optional, Self, Union, overload

from twitter_api.error import NeverError
from twitter_api.rate_limit.manager import DEFAULT_RATE_LIMIT_MANAGER
from twitter_api.rate_limit.manager.rate_limit_manager import RateLimitManager
from twitter_api.resources.oauth2_invalidate_token import (
    Oauth2InvalidateTokenResources,
    Oauth2InvalidateTokenUrl,
)
from twitter_api.resources.oauth2_token import Oauth2TokenResources, Oauth2TokenUrl
from twitter_api.resources.v2_dm_conversation_messages import (
    V2DmConversationMessagesResources,
    V2DmConversationsMessagesUrl,
)
from twitter_api.resources.v2_dm_conversations import (
    V2DmConversationsResources,
    V2DmConversationsUrl,
)
from twitter_api.resources.v2_dm_conversations_with_participant_dm_events import (
    V2DmConversationsWithParticipantDmEventsResources,
    V2DmConversationsWithParticipantDmEventsUrl,
)
from twitter_api.resources.v2_dm_conversations_with_participant_messages import (
    V2DmConversationsWithParticipantMessagesResources,
    V2DmConversationsWithParticipantMessagesUrl,
)
from twitter_api.resources.v2_tweet import V2TweetResources, V2TweetUrl
from twitter_api.resources.v2_tweet_retweeted_by import (
    V2TweetRetweetedByRerources,
    V2TweetRetweetedByUrl,
)
from twitter_api.resources.v2_tweets import V2TweetsResources, V2TweetsUrl
from twitter_api.resources.v2_tweets_search_all import (
    V2TweetsSearchAllResources,
    V2TweetsSearchAllUrl,
)
from twitter_api.resources.v2_tweets_search_recent import (
    V2TweetsSearchRecentResources,
    V2TweetsSearchRecentUrl,
)
from twitter_api.resources.v2_tweets_search_stream import (
    V2TweetsSearchStreamResources,
    V2TweetsSearchStreamUrl,
)
from twitter_api.resources.v2_tweets_search_stream_rules import (
    V2TweetsSearchStreamRulesResources,
    V2TweetsSearchStreamRulesUrl,
)
from twitter_api.resources.v2_user import V2UserResources, V2UserUrl
from twitter_api.resources.v2_user_followers import (
    V2UserFollowersResources,
    V2UserFollowersUrl,
)
from twitter_api.resources.v2_user_following import (
    V2UserFollowingResources,
    V2UserFollowingUrl,
)
from twitter_api.resources.v2_user_liked_tweets import (
    V2UserLikedTweetsResources,
    V2UserLikedTweetsUrl,
)
from twitter_api.resources.v2_user_retweets import (
    V2UserRetweetsResources,
    V2UserRetweetsUrl,
)
from twitter_api.resources.v2_user_tweets import V2UserTweetsResources, V2UserTweetsUrl
from twitter_api.resources.v2_users import V2UsersResources, V2UsersUrl
from twitter_api.resources.v2_users_by import V2UsersByResources, V2UsersByUrl
from twitter_api.resources.v2_users_by_username import (
    V2UsersByUsernameResources,
    V2UsersByUsernameUrl,
)
from twitter_api.types import httpx
from twitter_api.types._chainable import Chainable
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
from twitter_api.types.v2_scope import Scope

from .request.request_client import RequestClient


class TwitterApiClient(Chainable, metaclass=ABCMeta):
    """
    Twitter API を操作するためのクライアント
    """

    @property
    @abstractmethod
    def _request_client(self) -> RequestClient:
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
    ) -> V2TweetsSearchRecentResources:
        ...

    @overload
    def request(
        self: Self,
        url: V2TweetsSearchStreamUrl,
    ) -> V2TweetsSearchStreamResources:
        ...

    @overload
    def request(
        self: Self,
        url: V2TweetsSearchStreamRulesUrl,
    ) -> V2TweetsSearchStreamRulesResources:
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
        url: V2UsersByUrl,
    ) -> V2UsersByResources:
        ...

    @overload
    def request(
        self: Self,
        url: V2UsersByUsernameUrl,
    ) -> V2UsersByUsernameResources:
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
        url: V2DmConversationsWithParticipantDmEventsUrl,
    ) -> V2DmConversationsWithParticipantDmEventsResources:
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
            V2UserUrl,
            V2UsersUrl,
            V2UsersByUrl,
            V2UsersByUsernameUrl,
            V2DmConversationsWithParticipantDmEventsUrl,
            V2DmConversationsWithParticipantMessagesUrl,
            V2DmConversationsUrl,
            V2DmConversationsMessagesUrl,
        ],
    ):
        """
        操作したい URI を指定し、実行可能な操作方法を返却します。
        """

        if url == "https://api.twitter.com/oauth2/token":
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
            return V2TweetsSearchRecentResources(
                self._request_client,
            )
        elif url == "https://api.twitter.com/2/tweets/search/stream":
            return V2TweetsSearchStreamResources(
                self._request_client,
            )
        elif url == "https://api.twitter.com/2/tweets/search/stream/rules":
            return V2TweetsSearchStreamRulesResources(
                self._request_client,
            )
        elif url == "https://api.twitter.com/2/users":
            return V2UsersResources(
                self._request_client,
            )
        elif url == "https://api.twitter.com/2/users/by":
            return V2UsersByResources(
                self._request_client,
            )
        elif url == "https://api.twitter.com/2/users/by/username/:username":
            return V2UsersByUsernameResources(
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
            == "https://api.twitter.com/2/dm_conversations/with/:participant_id/dm_events"
        ):
            return V2DmConversationsWithParticipantDmEventsResources(
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
    def from_oauth2_bearer_token(
        cls,
        bearer_token: str,
        *,
        rate_limit_manager: RateLimitManager = DEFAULT_RATE_LIMIT_MANAGER,
        event_hooks: Optional[Mapping[str, list[httpx.EventHook]]] = None,
        limits: httpx.Limits = httpx.DEFAULT_LIMITS,
        mounts: Optional[Mapping[str, httpx.BaseTransport]] = None,
        proxies: Optional[httpx.ProxiesTypes] = None,
        timeout: httpx.TimeoutTypes = httpx.DEFAULT_TIMEOUT_CONFIG,
        transport: Optional[httpx.BaseTransport] = None,
        verify: httpx.VerifyTypes = True,
    ) -> Self:
        """OAuth 2.0 の Bearer 認証を用いてクライアントを作成する。"""

        from .twitter_api_real_client import TwitterApiRealClient

        return TwitterApiRealClient.from_oauth2_bearer_token(
            bearer_token,
            rate_limit_manager=rate_limit_manager,
            event_hooks=event_hooks,
            limits=limits,
            mounts=mounts,
            proxies=proxies,
            timeout=timeout,
            transport=transport,
            verify=verify,
        )

    @classmethod
    def from_oauth2_bearer_token_env(
        cls,
        bearer_token_env="BEARER_TOEKN",
        rate_limit_manager: RateLimitManager = DEFAULT_RATE_LIMIT_MANAGER,
        event_hooks: Optional[Mapping[str, list[httpx.EventHook]]] = None,
        limits: httpx.Limits = httpx.DEFAULT_LIMITS,
        mounts: Optional[Mapping[str, httpx.BaseTransport]] = None,
        proxies: Optional[httpx.ProxiesTypes] = None,
        timeout: httpx.TimeoutTypes = httpx.DEFAULT_TIMEOUT_CONFIG,
        transport: Optional[httpx.BaseTransport] = None,
        verify: httpx.VerifyTypes = True,
    ) -> Self:
        """環境変数から、 OAuth 2.0 の Bearer 認証を用いてクライアントを作成する。"""

        return cls.from_oauth2_bearer_token(
            cls._get_env(bearer_token_env),
            rate_limit_manager=rate_limit_manager,
            event_hooks=event_hooks,
            limits=limits,
            mounts=mounts,
            proxies=proxies,
            timeout=timeout,
            transport=transport,
            verify=verify,
        )

    @classmethod
    def from_oauth2_app(
        cls,
        *,
        api_key: ApiKey,
        api_secret: ApiSecret,
        rate_limit_manager: RateLimitManager = DEFAULT_RATE_LIMIT_MANAGER,
        event_hooks: Optional[Mapping[str, list[httpx.EventHook]]] = None,
        limits: httpx.Limits = httpx.DEFAULT_LIMITS,
        mounts: Optional[Mapping[str, httpx.BaseTransport]] = None,
        proxies: Optional[httpx.ProxiesTypes] = None,
        timeout: httpx.TimeoutTypes = httpx.DEFAULT_TIMEOUT_CONFIG,
        transport: Optional[httpx.BaseTransport] = None,
        verify: httpx.VerifyTypes = True,
    ) -> Self:
        """OAuth 2.0 のアプリ認証を用いてクライアントを作成する。"""

        from .twitter_api_real_client import TwitterApiRealClient

        return TwitterApiRealClient.from_oauth2_app(
            api_key=api_key,
            api_secret=api_secret,
            rate_limit_manager=rate_limit_manager,
            event_hooks=event_hooks,
            limits=limits,
            mounts=mounts,
            proxies=proxies,
            timeout=timeout,
            transport=transport,
            verify=verify,
        )

    @classmethod
    def from_oauth2_app_env(
        cls,
        *,
        api_key_env: Env[ApiKey] = "API_KEY",
        api_secret_env: Env[ApiSecret] = "API_SECRET",
        rate_limit_manager: RateLimitManager = DEFAULT_RATE_LIMIT_MANAGER,
        event_hooks: Optional[Mapping[str, list[httpx.EventHook]]] = None,
        limits: httpx.Limits = httpx.DEFAULT_LIMITS,
        mounts: Optional[Mapping[str, httpx.BaseTransport]] = None,
        proxies: Optional[httpx.ProxiesTypes] = None,
        timeout: httpx.TimeoutTypes = httpx.DEFAULT_TIMEOUT_CONFIG,
        transport: Optional[httpx.BaseTransport] = None,
        verify: httpx.VerifyTypes = True,
    ) -> Self:
        """環境変数から、OAuth 2.0 のアプリ認証を用いてクライアントを作成する。"""

        return cls.from_oauth2_app(
            api_key=cls._get_env(api_key_env),
            api_secret=cls._get_env(api_secret_env),
            rate_limit_manager=rate_limit_manager,
            event_hooks=event_hooks,
            limits=limits,
            mounts=mounts,
            proxies=proxies,
            timeout=timeout,
            transport=transport,
            verify=verify,
        )

    @classmethod
    def from_oauth2_user_flow(
        cls,
        *,
        client_id: ClientId,
        client_secret: ClientSecret,
        callback_url: CallbackUrl,
        scope: list[Scope],
        rate_limit_manager: RateLimitManager = DEFAULT_RATE_LIMIT_MANAGER,
        event_hooks: Optional[Mapping[str, list[httpx.EventHook]]] = None,
        limits: httpx.Limits = httpx.DEFAULT_LIMITS,
        mounts: Optional[Mapping[str, httpx.BaseTransport]] = None,
        proxies: Optional[httpx.ProxiesTypes] = None,
        timeout: httpx.TimeoutTypes = httpx.DEFAULT_TIMEOUT_CONFIG,
        transport: Optional[httpx.BaseTransport] = None,
        verify: httpx.VerifyTypes = True,
    ):
        """
        OAuth 2.0 のユーザ認証フローに従ってクライアントを作成する。
        """

        from .twitter_api_real_client import TwitterApiRealClient

        return TwitterApiRealClient.from_oauth2_user_flow(
            client_id=client_id,
            client_secret=client_secret,
            scope=scope,
            callback_url=callback_url,
            rate_limit_manager=rate_limit_manager,
            event_hooks=event_hooks,
            limits=limits,
            mounts=mounts,
            proxies=proxies,
            timeout=timeout,
            transport=transport,
            verify=verify,
        )

    @classmethod
    def from_oauth2_user_flow_env(
        cls,
        *,
        scope: list[Scope],
        client_id_env: Env[ClientId] = "CLIENT_ID",
        client_secret_env: Env[ClientSecret] = "CLIENT_SECRET",
        callback_url_env: Env[CallbackUrl] = "CALLBACK_URL",
        callback_url: Optional[CallbackUrl] = None,
        rate_limit_manager: RateLimitManager = DEFAULT_RATE_LIMIT_MANAGER,
        event_hooks: Optional[Mapping[str, list[httpx.EventHook]]] = None,
        limits: httpx.Limits = httpx.DEFAULT_LIMITS,
        mounts: Optional[Mapping[str, httpx.BaseTransport]] = None,
        proxies: Optional[httpx.ProxiesTypes] = None,
        timeout: httpx.TimeoutTypes = httpx.DEFAULT_TIMEOUT_CONFIG,
        transport: Optional[httpx.BaseTransport] = None,
        verify: httpx.VerifyTypes = True,
    ):
        """
        環境変数から、 OAuth 2.0 のユーザ認証フローに従ってクライアントを作成する。

        refer: https://developer.twitter.com/en/docs/authentication/oauth-2-0/authorization-code
        """

        return cls.from_oauth2_user_flow(
            client_id=cls._get_env(client_id_env),
            client_secret=cls._get_env(client_secret_env),
            scope=scope,
            callback_url=(
                callback_url
                if callback_url is not None
                else cls._get_env(callback_url_env)
            ),
            rate_limit_manager=rate_limit_manager,
            event_hooks=event_hooks,
            limits=limits,
            mounts=mounts,
            proxies=proxies,
            timeout=timeout,
            transport=transport,
            verify=verify,
        )

    @classmethod
    def from_oauth2_user_authorization_response_url(
        cls,
        *,
        authorization_response_url: CallbackUrl,
        state: str,
        code_verifier: str,
        client_id: ClientId,
        client_secret: ClientSecret,
        callback_url: CallbackUrl,
        rate_limit_manager: RateLimitManager = DEFAULT_RATE_LIMIT_MANAGER,
        event_hooks: Optional[Mapping[str, list[httpx.EventHook]]] = None,
        limits: httpx.Limits = httpx.DEFAULT_LIMITS,
        mounts: Optional[Mapping[str, httpx.BaseTransport]] = None,
        proxies: Optional[httpx.ProxiesTypes] = None,
        timeout: httpx.TimeoutTypes = httpx.DEFAULT_TIMEOUT_CONFIG,
        transport: Optional[httpx.BaseTransport] = None,
        verify: httpx.VerifyTypes = True,
    ):
        """
        OAuth 2.0 のユーザ認証フローの途中である、ユーザが認証後にリダイレクトされた CallbackUrl の段階からクライアントを作成する。

        refer: https://developer.twitter.com/en/docs/authentication/oauth-2-0/authorization-code
        """

        from .twitter_api_real_client import TwitterApiRealClient

        return TwitterApiRealClient.from_oauth2_user_authorization_response_url(
            authorization_response_url=authorization_response_url,
            client_id=client_id,
            client_secret=client_secret,
            callback_url=callback_url,
            state=state,
            code_verifier=code_verifier,
            rate_limit_manager=rate_limit_manager,
            event_hooks=event_hooks,
            limits=limits,
            mounts=mounts,
            proxies=proxies,
            timeout=timeout,
            transport=transport,
            verify=verify,
        )

    @classmethod
    def from_oauth2_user_authorization_response_url_env(
        cls,
        *,
        authorization_response_url: CallbackUrl,
        state: str,
        code_verifier: str,
        client_id_env: Env[ClientId] = "CLIENT_ID",
        client_secret_env: Env[ClientSecret] = "CLIENT_SECRET",
        callback_url_env: Env[CallbackUrl] = "CALLBACK_URL",
        callback_url: Optional[CallbackUrl] = None,
        rate_limit_manager: RateLimitManager = DEFAULT_RATE_LIMIT_MANAGER,
        event_hooks: Optional[Mapping[str, list[httpx.EventHook]]] = None,
        limits: httpx.Limits = httpx.DEFAULT_LIMITS,
        mounts: Optional[Mapping[str, httpx.BaseTransport]] = None,
        proxies: Optional[httpx.ProxiesTypes] = None,
        timeout: httpx.TimeoutTypes = httpx.DEFAULT_TIMEOUT_CONFIG,
        transport: Optional[httpx.BaseTransport] = None,
        verify: httpx.VerifyTypes = True,
    ):
        """
        環境変数から、OAuth 2.0 のユーザ認証フローの途中である、ユーザが認証後にリダイレクトされた CallbackUrl の段階からクライアントを作成する。

        refer: https://developer.twitter.com/en/docs/authentication/oauth-2-0/authorization-code
        """

        return cls.from_oauth2_user_authorization_response_url(
            authorization_response_url=authorization_response_url,
            state=state,
            code_verifier=code_verifier,
            client_id=cls._get_env(client_id_env),
            client_secret=cls._get_env(client_secret_env),
            callback_url=(
                callback_url
                if callback_url is not None
                else cls._get_env(callback_url_env)
            ),
            rate_limit_manager=rate_limit_manager,
            event_hooks=event_hooks,
            limits=limits,
            mounts=mounts,
            proxies=proxies,
            timeout=timeout,
            transport=transport,
            verify=verify,
        )

    @classmethod
    def from_oauth1_app(
        cls,
        *,
        api_key: ApiKey,
        api_secret: ApiSecret,
        access_token: AccessToken,
        access_secret: AccessSecret,
        rate_limit_manager: RateLimitManager = DEFAULT_RATE_LIMIT_MANAGER,
        event_hooks: Optional[Mapping[str, list[httpx.EventHook]]] = None,
        limits: httpx.Limits = httpx.DEFAULT_LIMITS,
        mounts: Optional[Mapping[str, httpx.BaseTransport]] = None,
        proxies: Optional[httpx.ProxiesTypes] = None,
        timeout: httpx.TimeoutTypes = httpx.DEFAULT_TIMEOUT_CONFIG,
        transport: Optional[httpx.BaseTransport] = None,
        verify: httpx.VerifyTypes = True,
    ) -> Self:
        """OAuth1.0a のアプリ認証を用いてクライアントを作成する。"""

        from .twitter_api_real_client import TwitterApiRealClient

        return TwitterApiRealClient.from_oauth1_app(
            api_key=api_key,
            api_secret=api_secret,
            access_token=access_token,
            access_secret=access_secret,
            rate_limit_manager=rate_limit_manager,
            event_hooks=event_hooks,
            limits=limits,
            mounts=mounts,
            proxies=proxies,
            timeout=timeout,
            transport=transport,
            verify=verify,
        )

    @classmethod
    def from_oauth1_app_env(
        cls,
        *,
        api_key_env: Env[ApiKey] = "API_KEY",
        api_secret_env: Env[ApiSecret] = "API_SECRET",
        access_token_env: Env[AccessToken] = "ACCESS_TOKEN",
        access_secret_env: Env[AccessSecret] = "ACCESS_SECRET",
        rate_limit_manager: RateLimitManager = DEFAULT_RATE_LIMIT_MANAGER,
        event_hooks: Optional[Mapping[str, list[httpx.EventHook]]] = None,
        limits: httpx.Limits = httpx.DEFAULT_LIMITS,
        mounts: Optional[Mapping[str, httpx.BaseTransport]] = None,
        proxies: Optional[httpx.ProxiesTypes] = None,
        timeout: httpx.TimeoutTypes = httpx.DEFAULT_TIMEOUT_CONFIG,
        transport: Optional[httpx.BaseTransport] = None,
        verify: httpx.VerifyTypes = True,
    ) -> Self:
        """環境変数から、OAuth1.0a のアプリ認証を用いてクライアントを作成する。"""

        return cls.from_oauth1_app(
            api_key=cls._get_env(api_key_env),
            api_secret=cls._get_env(api_secret_env),
            access_token=cls._get_env(access_token_env),
            access_secret=cls._get_env(access_secret_env),
            rate_limit_manager=rate_limit_manager,
            event_hooks=event_hooks,
            limits=limits,
            mounts=mounts,
            proxies=proxies,
            timeout=timeout,
            transport=transport,
            verify=verify,
        )

    @classmethod
    def from_oauth1_user_flow(
        cls,
        *,
        api_key: ApiKey,
        api_secret: ApiSecret,
        callback_url: CallbackUrl,
        rate_limit_manager: RateLimitManager = DEFAULT_RATE_LIMIT_MANAGER,
        event_hooks: Optional[Mapping[str, list[httpx.EventHook]]] = None,
        limits: httpx.Limits = httpx.DEFAULT_LIMITS,
        mounts: Optional[Mapping[str, httpx.BaseTransport]] = None,
        proxies: Optional[httpx.ProxiesTypes] = None,
        timeout: httpx.TimeoutTypes = httpx.DEFAULT_TIMEOUT_CONFIG,
        transport: Optional[httpx.BaseTransport] = None,
        verify: httpx.VerifyTypes = True,
    ):
        """
        OAuth 1.0a のユーザ認証フローに従ってクライアントを作成する。
        """

        from .twitter_api_real_client import TwitterApiRealClient

        return TwitterApiRealClient.from_oauth1_user_flow(
            api_key=api_key,
            api_secret=api_secret,
            callback_url=callback_url,
            rate_limit_manager=rate_limit_manager,
            event_hooks=event_hooks,
            limits=limits,
            mounts=mounts,
            proxies=proxies,
            timeout=timeout,
            transport=transport,
            verify=verify,
        )

    @classmethod
    def from_oauth1_user_flow_env(
        cls,
        *,
        api_key_env: Env[ApiKey] = "API_KEY",
        api_secret_env: Env[ApiSecret] = "API_SECRET",
        callback_url_env: Env[CallbackUrl] = "CALLBACK_URL",
        callback_url: Optional[CallbackUrl] = None,
        rate_limit_manager: RateLimitManager = DEFAULT_RATE_LIMIT_MANAGER,
        event_hooks: Optional[Mapping[str, list[httpx.EventHook]]] = None,
        limits: httpx.Limits = httpx.DEFAULT_LIMITS,
        mounts: Optional[Mapping[str, httpx.BaseTransport]] = None,
        proxies: Optional[httpx.ProxiesTypes] = None,
        timeout: httpx.TimeoutTypes = httpx.DEFAULT_TIMEOUT_CONFIG,
        transport: Optional[httpx.BaseTransport] = None,
        verify: httpx.VerifyTypes = True,
    ):
        """
        環境変数から、 OAuth 1.0a のユーザ認証フローに従ってクライアントを作成する。

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
            rate_limit_manager=rate_limit_manager,
            event_hooks=event_hooks,
            limits=limits,
            mounts=mounts,
            proxies=proxies,
            timeout=timeout,
            transport=transport,
            verify=verify,
        )

    @classmethod
    def from_oauth1_user_authorization_response_url(
        cls,
        *,
        authorization_response_url: CallbackUrl,
        api_key: ApiKey,
        api_secret: ApiSecret,
        callback_url: CallbackUrl,
        rate_limit_manager: RateLimitManager = DEFAULT_RATE_LIMIT_MANAGER,
        event_hooks: Optional[Mapping[str, list[httpx.EventHook]]] = None,
        limits: httpx.Limits = httpx.DEFAULT_LIMITS,
        mounts: Optional[Mapping[str, httpx.BaseTransport]] = None,
        proxies: Optional[httpx.ProxiesTypes] = None,
        timeout: httpx.TimeoutTypes = httpx.DEFAULT_TIMEOUT_CONFIG,
        transport: Optional[httpx.BaseTransport] = None,
        verify: httpx.VerifyTypes = True,
    ):
        """
        OAuth 1.0 のユーザ認証フローの途中である、ユーザが認証後にリダイレクトされた CallbackUrl の段階からクライアントを作成する。

        refer: https://developer.twitter.com/en/docs/authentication/oauth-1-0a/obtaining-user-access-tokens
        """

        from .twitter_api_real_client import TwitterApiRealClient

        return TwitterApiRealClient.from_oauth1_user_authorization_response_url(
            authorization_response_url=authorization_response_url,
            api_key=api_key,
            api_secret=api_secret,
            callback_url=callback_url,
            rate_limit_manager=rate_limit_manager,
            event_hooks=event_hooks,
            limits=limits,
            mounts=mounts,
            proxies=proxies,
            timeout=timeout,
            transport=transport,
            verify=verify,
        )

    @classmethod
    def from_oauth1_user_authorization_response_url_env(
        cls,
        *,
        authorization_response_url: CallbackUrl,
        api_key_env: Env[ApiKey] = "API_KEY",
        api_secret_env: Env[ApiSecret] = "API_SECRET",
        callback_url_env: Env[CallbackUrl] = "CALLBACK_URL",
        callback_url: Optional[CallbackUrl] = None,
        rate_limit_manager: RateLimitManager = DEFAULT_RATE_LIMIT_MANAGER,
        event_hooks: Optional[Mapping[str, list[httpx.EventHook]]] = None,
        limits: httpx.Limits = httpx.DEFAULT_LIMITS,
        mounts: Optional[Mapping[str, httpx.BaseTransport]] = None,
        proxies: Optional[httpx.ProxiesTypes] = None,
        timeout: httpx.TimeoutTypes = httpx.DEFAULT_TIMEOUT_CONFIG,
        transport: Optional[httpx.BaseTransport] = None,
        verify: httpx.VerifyTypes = True,
    ):
        """
        環境変数から、OAuth 1.0 のユーザ認証フローの途中である、ユーザが認証後にリダイレクトされた CallbackUrl の段階からクライアントを作成する。

        refer: https://developer.twitter.com/en/docs/authentication/oauth-1-0a/obtaining-user-access-tokens
        """

        return cls.from_oauth1_user_authorization_response_url(
            authorization_response_url=authorization_response_url,
            api_key=cls._get_env(api_key_env),
            api_secret=cls._get_env(api_secret_env),
            callback_url=(
                callback_url
                if callback_url is not None
                else cls._get_env(callback_url_env)
            ),
            rate_limit_manager=rate_limit_manager,
            event_hooks=event_hooks,
            limits=limits,
            mounts=mounts,
            proxies=proxies,
            timeout=timeout,
            transport=transport,
            verify=verify,
        )

    def close(self) -> None:
        pass

    def __enter__(self) -> Self:
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        pass

    @classmethod
    def _get_env(cls, key: Env[str]) -> str:
        """環境変数を取り出す。"""
        return os.environ[key]
