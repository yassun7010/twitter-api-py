from typing import Mapping, Optional, Self

from authlib.integrations.httpx_client.oauth1_client import OAuth1Auth
from authlib.integrations.httpx_client.oauth2_client import OAuth2Auth

from twitter_api.client.request.request_async_real_client import RequestAsyncRealClient
from twitter_api.client.request.request_real_client import RequestRealClient
from twitter_api.client.twitter_api_async_client import TwitterApiAsyncClient
from twitter_api.client.twitter_api_real_client import TwitterApiRealClient
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
)
from twitter_api.types.v2_scope import Scope

from .request.request_client import RequestClient


class TwitterApiAsyncRealClient(TwitterApiAsyncClient):
    """
    Twitter API V2 を操作するためのクライアント

    TwitterApiClient から生成されるクラスは、このクラスを継承する。
    """

    def __init__(
        self,
        request_client: RequestAsyncRealClient,
    ) -> None:
        self._real_request_client = request_client

    @property
    def _request_client(self) -> RequestClient:
        return self._real_request_client

    @classmethod
    def from_oauth2_bearer_token(
        cls,
        bearer_token: str,
        rate_limit_manager: RateLimitManager = DEFAULT_RATE_LIMIT_MANAGER,
        event_hooks: Optional[Mapping[str, list[httpx.EventHook]]] = None,
        limits: httpx.Limits = httpx.DEFAULT_LIMITS,
        mounts: Optional[Mapping[str, httpx.AsyncBaseTransport]] = None,
        proxies: Optional[httpx.ProxiesTypes] = None,
        timeout: httpx.TimeoutTypes = httpx.DEFAULT_TIMEOUT_CONFIG,
        transport: Optional[httpx.AsyncBaseTransport] = None,
        verify: httpx.VerifyTypes = True,
    ):
        return TwitterApiAsyncRealClient(
            RequestAsyncRealClient(
                auth=OAuth2Auth(
                    token={
                        "access_token": bearer_token,
                        "token_type": "Bearer",
                    }
                ),
                oauth_version="2.0",
                rate_limit_target="app",
                rate_limit_manager=rate_limit_manager,
                event_hooks=event_hooks,
                limits=limits,
                mounts=mounts,
                proxies=proxies,
                timeout=timeout,
                transport=transport,
                verify=verify,
            ),
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
    ):
        with TwitterApiRealClient(
            RequestRealClient(
                auth=None,
                oauth_version="2.0",
                rate_limit_target="app",
                rate_limit_manager=rate_limit_manager,
                event_hooks=event_hooks,
                limits=limits,
                mounts=None,
                proxies=proxies,
                timeout=timeout,
                transport=None,
                verify=verify,
            ),
        ) as client:
            access_token = (
                client.request("https://api.twitter.com/oauth2/token")
                .post(
                    api_key=api_key,
                    api_secret=api_secret,
                    query={"grant_type": "client_credentials"},
                )
                .access_token
            )

        return TwitterApiAsyncRealClient.from_oauth2_bearer_token(
            access_token,
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
        mounts: Optional[Mapping[str, httpx.AsyncBaseTransport]] = None,
        proxies: Optional[httpx.ProxiesTypes] = None,
        timeout: httpx.TimeoutTypes = httpx.DEFAULT_TIMEOUT_CONFIG,
        transport: Optional[httpx.AsyncBaseTransport] = None,
        verify: httpx.VerifyTypes = True,
    ):
        from twitter_api.client.oauth_flow.twitter_oauth2_authorization_client import (
            TwitterOAuth2AuthorizeClient,
        )
        from twitter_api.client.oauth_session.twitter_oauth2_real_session import (
            TwitterOAuth2RealSession,
        )

        session: TwitterOAuth2RealSession[
            TwitterApiAsyncRealClient
        ] = TwitterOAuth2RealSession(
            client_generator=lambda access_token: TwitterApiAsyncRealClient.from_oauth2_bearer_token(
                access_token,
                rate_limit_manager=rate_limit_manager,
                event_hooks=event_hooks,
                limits=limits,
                mounts=mounts,
                proxies=proxies,
                timeout=timeout,
                transport=transport,
                verify=verify,
            ),
            client_id=client_id,
            client_secret=client_secret,
            callback_url=callback_url,
            scope=scope,
            event_hooks=event_hooks,
            limits=limits,
            mounts=None,
            proxies=proxies,
            timeout=timeout,
            transport=None,
            verify=verify,
        )

        client: TwitterOAuth2AuthorizeClient[
            TwitterApiAsyncRealClient
        ] = TwitterOAuth2AuthorizeClient(session)

        return client

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
        from twitter_api.client.oauth_flow.twitter_oauth2_access_token_client import (
            TwitterOAuth2AccessTokenClient,
        )
        from twitter_api.client.oauth_session.twitter_oauth2_real_session import (
            TwitterOAuth2RealSession,
        )

        from .twitter_api_async_real_client import TwitterApiAsyncRealClient

        session: TwitterOAuth2RealSession[
            TwitterApiAsyncRealClient
        ] = TwitterOAuth2RealSession(
            lambda access_token: TwitterApiAsyncRealClient.from_oauth2_bearer_token(
                access_token,
                rate_limit_manager=rate_limit_manager,
                event_hooks=event_hooks,
                limits=limits,
                mounts=mounts,
                proxies=proxies,
                timeout=timeout,
                transport=transport,
                verify=verify,
            ),
            client_id=client_id,
            client_secret=client_secret,
            callback_url=callback_url,
            scope=None,
            event_hooks=event_hooks,
            limits=limits,
            mounts=None,
            proxies=proxies,
            timeout=timeout,
            transport=None,
            verify=verify,
        )

        client: TwitterOAuth2AccessTokenClient[
            TwitterApiAsyncRealClient
        ] = TwitterOAuth2AccessTokenClient(
            authorization_response_url=authorization_response_url,
            state=state,
            code_verifier=code_verifier,
            session=session,
        )

        return client

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
        return TwitterApiAsyncRealClient(
            RequestAsyncRealClient(
                auth=OAuth1Auth(
                    client_id=api_key,
                    client_secret=api_secret,
                    token=access_token,
                    token_secret=access_secret,
                    force_include_body=True,
                ),
                oauth_version="1.0a",
                rate_limit_target="user",
                rate_limit_manager=rate_limit_manager,
                event_hooks=event_hooks,
                limits=limits,
                mounts=mounts,
                proxies=proxies,
                timeout=timeout,
                transport=transport,
                verify=verify,
            ),
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
        from twitter_api.client.oauth_flow.twitter_oauth1_request_token_client import (
            TwitterOAuth1RequestTokenClient,
        )
        from twitter_api.client.oauth_session.twitter_oauth1_real_session import (
            TwitterOAuth1RealSession,
        )

        session = TwitterOAuth1RealSession(
            lambda access_token, access_secret: TwitterApiAsyncRealClient.from_oauth1_app(
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
            ),
            api_key=api_key,
            api_secret=api_secret,
            callback_url=callback_url,
            event_hooks=event_hooks,
            limits=limits,
            mounts=None,
            proxies=proxies,
            timeout=timeout,
            transport=None,
            verify=verify,
        )

        return TwitterOAuth1RequestTokenClient(session)

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
        from twitter_api.client.oauth_flow.twitter_oauth1_access_token_client import (
            TwitterOAuth1AccessTokenClient,
        )
        from twitter_api.client.oauth_session.twitter_oauth1_real_session import (
            TwitterOAuth1RealSession,
        )

        session = TwitterOAuth1RealSession(
            lambda access_token, access_secret: TwitterApiAsyncRealClient.from_oauth1_app(
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
            ),
            api_key=api_key,
            api_secret=api_secret,
            callback_url=callback_url,
            event_hooks=event_hooks,
            limits=limits,
            mounts=None,
            proxies=proxies,
            timeout=timeout,
            transport=None,
            verify=verify,
        )

        return TwitterOAuth1AccessTokenClient(
            authorization_response_url=authorization_response_url,
            session=session,
        )

    async def aclose(self) -> None:
        await self._real_request_client.aclose()

    async def __aenter__(self) -> Self:
        await self._real_request_client.__aenter__()
        return self

    async def __aexit__(self, exc_type, exc_value, traceback) -> None:
        await self._real_request_client.__aexit__(exc_type, exc_value, traceback)
