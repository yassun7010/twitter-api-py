from typing import Mapping, Optional, Self

from twitter_api.client.twitter_api_async_client import TwitterApiAsyncClient
from twitter_api.rate_limit.manager import DEFAULT_RATE_LIMIT_MANAGER
from twitter_api.rate_limit.manager.rate_limit_manager import RateLimitManager
from twitter_api.types import httpx
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

from .twitter_api_mock_client import _BaseTwitterApiMockClient


class TwitterApiAsyncMockClient(_BaseTwitterApiMockClient, TwitterApiAsyncClient):
    @classmethod
    def from_oauth2_bearer_token(
        cls,
        bearer_token: str,
        *,
        rate_limit_manager: RateLimitManager = DEFAULT_RATE_LIMIT_MANAGER,
        event_hooks: Optional[Mapping[str, list[httpx.EventHook]]] = None,
        limits: httpx.Limits = httpx.DEFAULT_LIMITS,
        mounts: Optional[Mapping[str, httpx.AsyncBaseTransport]] = None,
        proxies: Optional[httpx.ProxiesTypes] = None,
        timeout: httpx.TimeoutTypes = httpx.DEFAULT_TIMEOUT_CONFIG,
        transport: Optional[httpx.AsyncBaseTransport] = None,
        verify: httpx.VerifyTypes = True,
    ):
        return TwitterApiAsyncMockClient(
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
        mounts: Optional[Mapping[str, httpx.AsyncBaseTransport]] = None,
        proxies: Optional[httpx.ProxiesTypes] = None,
        timeout: httpx.TimeoutTypes = httpx.DEFAULT_TIMEOUT_CONFIG,
        transport: Optional[httpx.AsyncBaseTransport] = None,
        verify: httpx.VerifyTypes = True,
    ) -> Self:
        return TwitterApiAsyncMockClient(
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
        mounts: Optional[Mapping[str, httpx.AsyncBaseTransport]] = None,
        proxies: Optional[httpx.ProxiesTypes] = None,
        timeout: httpx.TimeoutTypes = httpx.DEFAULT_TIMEOUT_CONFIG,
        transport: Optional[httpx.AsyncBaseTransport] = None,
        verify: httpx.VerifyTypes = True,
    ):
        from twitter_api.client.oauth_flow.twitter_oauth2_authorization_mock_client import (
            TwitterOAuth2AuthorizeMockClient,
        )
        from twitter_api.client.oauth_session.twitter_oauth2_mock_session import (
            TwitterOAuth2MockSession,
        )

        session = TwitterOAuth2MockSession(
            lambda access_token: TwitterApiAsyncMockClient.from_oauth2_bearer_token(
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
        event_hooks: Optional[Mapping[str, list[httpx.EventHook]]] = None,
        limits: httpx.Limits = httpx.DEFAULT_LIMITS,
        mounts: Optional[Mapping[str, httpx.AsyncBaseTransport]] = None,
        proxies: Optional[httpx.ProxiesTypes] = None,
        timeout: httpx.TimeoutTypes = httpx.DEFAULT_TIMEOUT_CONFIG,
        transport: Optional[httpx.AsyncBaseTransport] = None,
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
        mounts: Optional[Mapping[str, httpx.AsyncBaseTransport]] = None,
        proxies: Optional[httpx.ProxiesTypes] = None,
        timeout: httpx.TimeoutTypes = httpx.DEFAULT_TIMEOUT_CONFIG,
        transport: Optional[httpx.AsyncBaseTransport] = None,
        verify: httpx.VerifyTypes = True,
    ):
        from twitter_api.client.oauth_flow.twitter_oauth2_access_token_mock_client import (
            TwitterOAuth2AccessTokenMockClient,
        )
        from twitter_api.client.oauth_session.twitter_oauth2_mock_session import (
            TwitterOAuth2MockSession,
        )

        session = TwitterOAuth2MockSession(
            lambda access_token: TwitterApiAsyncMockClient.from_oauth2_bearer_token(
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
        client_id_env: Env[ClientId],
        client_secret_env: Env[ClientSecret],
        callback_url_env: Env[CallbackUrl],
        callback_url: Optional[CallbackUrl] = None,
        rate_limit_manager: RateLimitManager = DEFAULT_RATE_LIMIT_MANAGER,
        event_hooks: Optional[Mapping[str, list[httpx.EventHook]]] = None,
        limits: httpx.Limits = httpx.DEFAULT_LIMITS,
        mounts: Optional[Mapping[str, httpx.AsyncBaseTransport]] = None,
        proxies: Optional[httpx.ProxiesTypes] = None,
        timeout: httpx.TimeoutTypes = httpx.DEFAULT_TIMEOUT_CONFIG,
        transport: Optional[httpx.AsyncBaseTransport] = None,
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
        mounts: Optional[Mapping[str, httpx.AsyncBaseTransport]] = None,
        proxies: Optional[httpx.ProxiesTypes] = None,
        timeout: httpx.TimeoutTypes = httpx.DEFAULT_TIMEOUT_CONFIG,
        transport: Optional[httpx.AsyncBaseTransport] = None,
        verify: httpx.VerifyTypes = True,
    ):
        return TwitterApiAsyncMockClient(
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
        mounts: Optional[Mapping[str, httpx.AsyncBaseTransport]] = None,
        proxies: Optional[httpx.ProxiesTypes] = None,
        timeout: httpx.TimeoutTypes = httpx.DEFAULT_TIMEOUT_CONFIG,
        transport: Optional[httpx.AsyncBaseTransport] = None,
        verify: httpx.VerifyTypes = True,
    ):
        from twitter_api.client.oauth_flow.twitter_oauth1_request_token_mock_client import (
            TwitterOAuth1RequestTokenMockClient,
        )
        from twitter_api.client.oauth_session.twitter_oauth1_mock_session import (
            TwitterOAuth1MockSession,
        )

        session = TwitterOAuth1MockSession(
            lambda access_token, access_secret: TwitterApiAsyncMockClient.from_oauth1_app(
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
        event_hooks: Optional[Mapping[str, list[httpx.EventHook]]] = None,
        limits: httpx.Limits = httpx.DEFAULT_LIMITS,
        mounts: Optional[Mapping[str, httpx.AsyncBaseTransport]] = None,
        proxies: Optional[httpx.ProxiesTypes] = None,
        timeout: httpx.TimeoutTypes = httpx.DEFAULT_TIMEOUT_CONFIG,
        transport: Optional[httpx.AsyncBaseTransport] = None,
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
        mounts: Optional[Mapping[str, httpx.AsyncBaseTransport]] = None,
        proxies: Optional[httpx.ProxiesTypes] = None,
        timeout: httpx.TimeoutTypes = httpx.DEFAULT_TIMEOUT_CONFIG,
        transport: Optional[httpx.AsyncBaseTransport] = None,
        verify: httpx.VerifyTypes = True,
    ):
        from twitter_api.client.oauth_flow.twitter_oauth1_access_token_mock_client import (
            TwitterOAuth1AccessTokenMockClient,
        )
        from twitter_api.client.oauth_session.twitter_oauth1_mock_session import (
            TwitterOAuth1MockSession,
        )

        session = TwitterOAuth1MockSession(
            lambda access_token, access_secret: TwitterApiAsyncMockClient.from_oauth1_app(
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
        mounts: Optional[Mapping[str, httpx.AsyncBaseTransport]] = None,
        proxies: Optional[httpx.ProxiesTypes] = None,
        timeout: httpx.TimeoutTypes = httpx.DEFAULT_TIMEOUT_CONFIG,
        transport: Optional[httpx.AsyncBaseTransport] = None,
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
