from typing import Mapping, Optional, Self, Union, overload

from twitter_api.error import TwitterApiError
from twitter_api.rate_limit.manager import DEFAULT_RATE_LIMIT_MANAGER
from twitter_api.rate_limit.manager.rate_limit_manager import RateLimitManager
from twitter_api.rate_limit.rate_limit_target import RateLimitTarget
from twitter_api.resources.oauth2_invalidate_token import Oauth2InvalidateTokenUrl
from twitter_api.resources.oauth2_invalidate_token.post_oauth2_invalidate_token import (
    PostOauth2InvalidateTokenResponseBody,
)
from twitter_api.resources.oauth2_token import Oauth2TokenUrl
from twitter_api.resources.oauth2_token.post_oauth2_token import (
    PostOauth2TokenResponseBody,
)
from twitter_api.resources.v2_dm_conversation_messages import (
    V2DmConversationsMessagesUrl,
)
from twitter_api.resources.v2_dm_conversation_messages.post_v2_dm_conversations_messages import (
    PostV2DmConversationMessagesResponseBody,
)
from twitter_api.resources.v2_dm_conversations import V2DmConversationsUrl
from twitter_api.resources.v2_dm_conversations.post_v2_dm_conversations import (
    PostV2DmConversationsResponseBody,
)
from twitter_api.resources.v2_dm_conversations_with_participant_dm_events import (
    V2DmConversationsWithParticipantDmEventsUrl,
)
from twitter_api.resources.v2_dm_conversations_with_participant_dm_events.get_v2_dm_conversations_with_participant_dm_events import (
    GetV2DmConversationsWithParticipantDmEventsResponseBody,
)
from twitter_api.resources.v2_dm_conversations_with_participant_messages import (
    V2DmConversationsWithParticipantMessagesUrl,
)
from twitter_api.resources.v2_dm_conversations_with_participant_messages.post_v2_dm_conversations_with_participant_messages import (
    PostV2DmConversationsWithParticipantMessagesResponseBody,
)
from twitter_api.resources.v2_tweet import V2TweetUrl
from twitter_api.resources.v2_tweet.delete_v2_tweet import DeleteV2TweetResponseBody
from twitter_api.resources.v2_tweet.get_v2_tweet import GetV2TweetResponseBody
from twitter_api.resources.v2_tweet_retweeted_by import V2TweetRetweetedByUrl
from twitter_api.resources.v2_tweet_retweeted_by.get_v2_tweet_retweeted_by import (
    GetV2TweetRetweetedByResponseBody,
)
from twitter_api.resources.v2_tweets import V2TweetsUrl
from twitter_api.resources.v2_tweets.get_v2_tweets import GetV2TweetsResponseBody
from twitter_api.resources.v2_tweets.post_v2_tweets import PostV2TweetsResponseBody
from twitter_api.resources.v2_tweets_search_all import V2TweetsSearchAllUrl
from twitter_api.resources.v2_tweets_search_all.get_v2_tweets_search_all import (
    GetV2TweetsSearchAllResponseBody,
)
from twitter_api.resources.v2_tweets_search_recent import V2TweetsSearchRecentUrl
from twitter_api.resources.v2_tweets_search_recent.get_v2_tweets_search_recent import (
    GetV2TweetsSearchRecentResponseBody,
)
from twitter_api.resources.v2_tweets_search_stream import V2TweetsSearchStreamUrl
from twitter_api.resources.v2_tweets_search_stream.get_v2_tweets_search_stream import (
    GetV2TweetsSearchStreamResponseBody,
)
from twitter_api.resources.v2_tweets_search_stream_rules import (
    V2TweetsSearchStreamRulesUrl,
)
from twitter_api.resources.v2_tweets_search_stream_rules.get_v2_tweets_search_stream_rules import (
    GetV2TweetsSearchStreamRulesResponseBody,
)
from twitter_api.resources.v2_tweets_search_stream_rules.post_v2_tweets_search_stream_rules import (
    PostV2TweetsSearchStreamRulesResponseBody,
)
from twitter_api.resources.v2_user import V2UserUrl
from twitter_api.resources.v2_user.get_v2_user import GetV2UserResponseBody
from twitter_api.resources.v2_user_followers import V2UserFollowersUrl
from twitter_api.resources.v2_user_followers.get_v2_user_followers import (
    GetV2UserFollowersResponseBody,
)
from twitter_api.resources.v2_user_following import V2UserFollowingUrl
from twitter_api.resources.v2_user_following.post_v2_user_following import (
    PostV2UserFollowingResponseBody,
)
from twitter_api.resources.v2_user_liked_tweets import V2UserLikedTweetsUrl
from twitter_api.resources.v2_user_liked_tweets.get_v2_user_liked_tweets import (
    GetV2UserLikedTweetsResponseBody,
)
from twitter_api.resources.v2_user_retweets import V2UserRetweetsUrl
from twitter_api.resources.v2_user_retweets.post_v2_user_retweets import (
    PostV2UserRetweetsResponseBody,
)
from twitter_api.resources.v2_user_tweets import V2UserTweetsUrl
from twitter_api.resources.v2_user_tweets.get_v2_user_tweets import (
    GetV2UserTweetsResponseBody,
)
from twitter_api.resources.v2_users import V2UsersUrl
from twitter_api.resources.v2_users.get_v2_users import GetV2UsersResponseBody
from twitter_api.resources.v2_users_by import V2UsersByUrl
from twitter_api.resources.v2_users_by.get_v2_users_by import GetV2UsersByResponseBody
from twitter_api.resources.v2_users_by_username import V2UsersByUsernameUrl
from twitter_api.resources.v2_users_by_username.get_v2_users_by_username import (
    GetV2UsersByUsernameResponseBody,
)
from twitter_api.types import httpx
from twitter_api.types.endpoint import Endpoint
from twitter_api.types.oauth import (
    AccessSecret,
    AccessToken,
    ApiKey,
    ApiSecret,
    CallbackUrl,
    ClientId,
    ClientSecret,
    Env,
    OAuthVersion,
)
from twitter_api.types.v2_scope import Scope

from .request.request_client import RequestClient
from .request.request_mock_client import RequestMockClient
from .twitter_api_client import TwitterApiClient


class _BaseTwitterApiMockClient:
    def __init__(
        self,
        *,
        oauth_version: OAuthVersion,
        rate_limit_target: RateLimitTarget,
        rate_limit_manager: RateLimitManager = DEFAULT_RATE_LIMIT_MANAGER,
    ) -> None:
        self._client = RequestMockClient(
            oauth_version=oauth_version,
            rate_limit_target=rate_limit_target,
            rate_limit_manager=rate_limit_manager,
        )

    @property
    def _request_client(self) -> RequestClient:
        return self._client

    @overload
    def inject_get_response_body(
        self,
        url: V2TweetsUrl,
        response_body: Union[
            GetV2TweetsResponseBody,
            TwitterApiError,
        ],
    ) -> Self:
        ...

    @overload
    def inject_get_response_body(
        self,
        url: V2TweetUrl,
        response_body: Union[
            GetV2TweetResponseBody,
            TwitterApiError,
        ],
    ) -> Self:
        ...

    @overload
    def inject_get_response_body(
        self,
        url: V2TweetRetweetedByUrl,
        response_body: Union[
            GetV2TweetRetweetedByResponseBody,
            TwitterApiError,
        ],
    ) -> Self:
        ...

    @overload
    def inject_get_response_body(
        self,
        url: V2TweetsSearchAllUrl,
        response_body: Union[
            GetV2TweetsSearchAllResponseBody,
            TwitterApiError,
        ],
    ) -> Self:
        ...

    @overload
    def inject_get_response_body(
        self,
        url: V2TweetsSearchRecentUrl,
        response_body: Union[
            GetV2TweetsSearchRecentResponseBody,
            TwitterApiError,
        ],
    ) -> Self:
        ...

    @overload
    def inject_get_response_body(
        self,
        url: V2TweetsSearchStreamUrl,
        response_body: Union[
            GetV2TweetsSearchStreamResponseBody,
            TwitterApiError,
        ],
    ) -> Self:
        ...

    @overload
    def inject_get_response_body(
        self,
        url: V2TweetsSearchStreamRulesUrl,
        response_body: Union[
            GetV2TweetsSearchStreamRulesResponseBody,
            TwitterApiError,
        ],
    ) -> Self:
        ...

    @overload
    def inject_get_response_body(
        self,
        url: V2UsersUrl,
        response_body: Union[
            GetV2UsersResponseBody,
            TwitterApiError,
        ],
    ) -> Self:
        ...

    @overload
    def inject_get_response_body(
        self,
        url: V2UsersByUrl,
        response_body: Union[
            GetV2UsersByResponseBody,
            TwitterApiError,
        ],
    ) -> Self:
        ...

    @overload
    def inject_get_response_body(
        self,
        url: V2UsersByUsernameUrl,
        response_body: Union[
            GetV2UsersByUsernameResponseBody,
            TwitterApiError,
        ],
    ) -> Self:
        ...

    @overload
    def inject_get_response_body(
        self,
        url: V2UserUrl,
        response_body: Union[
            GetV2UserResponseBody,
            TwitterApiError,
        ],
    ) -> Self:
        ...

    @overload
    def inject_get_response_body(
        self,
        url: V2UserLikedTweetsUrl,
        response_body: Union[
            GetV2UserLikedTweetsResponseBody,
            TwitterApiError,
        ],
    ) -> Self:
        ...

    @overload
    def inject_get_response_body(
        self,
        url: V2UserFollowersUrl,
        response_body: Union[
            GetV2UserFollowersResponseBody,
            TwitterApiError,
        ],
    ) -> Self:
        ...

    @overload
    def inject_get_response_body(
        self,
        url: V2UserTweetsUrl,
        response_body: Union[
            GetV2UserTweetsResponseBody,
            TwitterApiError,
        ],
    ) -> Self:
        ...

    @overload
    def inject_get_response_body(
        self,
        url: V2DmConversationsWithParticipantDmEventsUrl,
        response_body: Union[
            GetV2DmConversationsWithParticipantDmEventsResponseBody,
            TwitterApiError,
        ],
    ) -> Self:
        ...

    def inject_get_response_body(self, url, response_body) -> Self:
        self._client.inject_response_body(Endpoint("GET", url), response_body)

        return self

    @overload
    def inject_post_response_body(
        self,
        url: Oauth2InvalidateTokenUrl,
        response_body: Union[
            PostOauth2InvalidateTokenResponseBody,
            TwitterApiError,
        ],
    ) -> Self:
        ...

    @overload
    def inject_post_response_body(
        self,
        url: Oauth2TokenUrl,
        response_body: Union[
            PostOauth2TokenResponseBody,
            TwitterApiError,
        ],
    ) -> Self:
        ...

    @overload
    def inject_post_response_body(
        self,
        url: V2TweetsUrl,
        response_body: Union[
            PostV2TweetsResponseBody,
            TwitterApiError,
        ],
    ) -> Self:
        ...

    @overload
    def inject_post_response_body(
        self,
        url: V2TweetsSearchStreamRulesUrl,
        response_body: Union[
            PostV2TweetsSearchStreamRulesResponseBody,
            TwitterApiError,
        ],
    ) -> Self:
        ...

    @overload
    def inject_post_response_body(
        self,
        url: V2UserFollowingUrl,
        response_body: Union[
            PostV2UserFollowingResponseBody,
            TwitterApiError,
        ],
    ) -> Self:
        ...

    @overload
    def inject_post_response_body(
        self,
        url: V2UserRetweetsUrl,
        response_body: Union[
            PostV2UserRetweetsResponseBody,
            TwitterApiError,
        ],
    ) -> Self:
        ...

    @overload
    def inject_post_response_body(
        self,
        url: V2DmConversationsWithParticipantMessagesUrl,
        response_body: Union[
            PostV2DmConversationsWithParticipantMessagesResponseBody,
            TwitterApiError,
        ],
    ) -> Self:
        ...

    @overload
    def inject_post_response_body(
        self,
        url: V2DmConversationsUrl,
        response_body: Union[
            PostV2DmConversationsResponseBody,
            TwitterApiError,
        ],
    ) -> Self:
        ...

    @overload
    def inject_post_response_body(
        self,
        url: V2DmConversationsMessagesUrl,
        response_body: Union[
            PostV2DmConversationMessagesResponseBody,
            TwitterApiError,
        ],
    ) -> Self:
        ...

    def inject_post_response_body(self, url, response_body) -> Self:
        self._client.inject_response_body(Endpoint("POST", url), response_body)

        return self

    def inject_delete_response_body(
        self,
        url: V2TweetUrl,
        response_body: Union[
            DeleteV2TweetResponseBody,
            TwitterApiError,
        ],
    ) -> Self:
        self._client.inject_response_body(Endpoint("DELETE", url), response_body)

        return self

    @classmethod
    def _get_env(cls, key: Env[str]) -> str:
        """
        環境変数を取り出す。

        Mock であるためとりあえず値を返す。
        """

        return ""


class TwitterApiMockClient(_BaseTwitterApiMockClient, TwitterApiClient):
    """Twitter API V2 をモックするためのクライアント"""

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
    ):
        return TwitterApiMockClient(
            oauth_version="2.0",
            rate_limit_target="app",
            rate_limit_manager=rate_limit_manager,
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
        return TwitterApiMockClient(
            oauth_version="2.0",
            rate_limit_target="app",
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
        rate_limit_manager: RateLimitManager = DEFAULT_RATE_LIMIT_MANAGER,
        event_hooks: Optional[Mapping[str, list[httpx.EventHook]]] = None,
        limits: httpx.Limits = httpx.DEFAULT_LIMITS,
        mounts: Optional[Mapping[str, httpx.BaseTransport]] = None,
        proxies: Optional[httpx.ProxiesTypes] = None,
        timeout: httpx.TimeoutTypes = httpx.DEFAULT_TIMEOUT_CONFIG,
        transport: Optional[httpx.BaseTransport] = None,
        verify: httpx.VerifyTypes = True,
    ):
        from twitter_api.client.oauth_flow.twitter_oauth2_authorization_mock_client import (
            TwitterOAuth2AuthorizeMockClient,
        )
        from twitter_api.client.oauth_session.twitter_oauth2_mock_session import (
            TwitterOAuth2MockSession,
        )

        session = TwitterOAuth2MockSession(
            lambda access_token: TwitterApiMockClient.from_oauth2_bearer_token(
                access_token
            ),
            scope=scope,
        )

        return TwitterOAuth2AuthorizeMockClient(session=session)

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
        from twitter_api.client.oauth_flow.twitter_oauth2_access_token_mock_client import (
            TwitterOAuth2AccessTokenMockClient,
        )
        from twitter_api.client.oauth_session.twitter_oauth2_mock_session import (
            TwitterOAuth2MockSession,
        )

        session = TwitterOAuth2MockSession(
            lambda access_token: TwitterApiMockClient.from_oauth2_bearer_token(
                access_token,
            ),
            scope=[],
        )

        return TwitterOAuth2AccessTokenMockClient(
            authorization_response_url=authorization_response_url,
            state=state,
            code_verifier=code_verifier,
            session=session,
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
    ):
        return TwitterApiMockClient(
            oauth_version="1.0a",
            rate_limit_target="app",
            rate_limit_manager=rate_limit_manager,
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
        from twitter_api.client.oauth_flow.twitter_oauth1_request_token_mock_client import (
            TwitterOAuth1RequestTokenMockClient,
        )
        from twitter_api.client.oauth_session.twitter_oauth1_mock_session import (
            TwitterOAuth1MockSession,
        )

        session = TwitterOAuth1MockSession(
            lambda access_token, access_secret: TwitterApiMockClient.from_oauth1_app(
                api_key=api_key,
                api_secret=api_secret,
                access_token=access_token,
                access_secret=access_secret,
            ),
        )

        return TwitterOAuth1RequestTokenMockClient(session=session)

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
        from twitter_api.client.oauth_flow.twitter_oauth1_access_token_mock_client import (
            TwitterOAuth1AccessTokenMockClient,
        )
        from twitter_api.client.oauth_session.twitter_oauth1_mock_session import (
            TwitterOAuth1MockSession,
        )

        session: TwitterOAuth1MockSession[
            TwitterApiMockClient
        ] = TwitterOAuth1MockSession(
            lambda access_token, access_secret: TwitterApiMockClient.from_oauth1_app(
                api_key=api_key,
                api_secret=api_secret,
                access_token=access_token,
                access_secret=access_secret,
            ),
        )

        return TwitterOAuth1AccessTokenMockClient(
            authorization_response_url=authorization_response_url,
            session=session,
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
