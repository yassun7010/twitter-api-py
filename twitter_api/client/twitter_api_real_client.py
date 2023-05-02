from typing import Mapping, Optional, Self

from authlib.integrations.httpx_client.oauth1_client import OAuth1Auth
from authlib.integrations.httpx_client.oauth2_client import OAuth2Auth

from twitter_api.client.oauth_flow.twitter_oauth1_request_token_client import (
    TwitterOAuth1RequestTokenClient,
)
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
from .request.request_real_client import RequestRealClient
from .twitter_api_client import TwitterApiClient


class TwitterApiRealClient(TwitterApiClient):
    """
    Twitter API V2 を操作するためのクライアント
    """

    def __init__(
        self,
        request_client: RequestRealClient,
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
        mounts: Optional[Mapping[str, httpx.BaseTransport]] = None,
        proxies: Optional[httpx.ProxiesTypes] = None,
        timeout: httpx.TimeoutTypes = httpx.DEFAULT_TIMEOUT_CONFIG,
        transport: Optional[httpx.BaseTransport] = None,
        verify: httpx.VerifyTypes = True,
    ):
        return TwitterApiRealClient(
            RequestRealClient(
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
        mounts: Optional[Mapping[str, httpx.BaseTransport]] = None,
        proxies: Optional[httpx.ProxiesTypes] = None,
        timeout: httpx.TimeoutTypes = httpx.DEFAULT_TIMEOUT_CONFIG,
        transport: Optional[httpx.BaseTransport] = None,
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
                mounts=mounts,
                proxies=proxies,
                timeout=timeout,
                transport=transport,
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

        return TwitterApiRealClient.from_oauth2_bearer_token(access_token)

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
        from twitter_api.client.oauth_flow.twitter_oauth2_authorization_client import (
            TwitterOAuth2AuthorizeClient,
        )
        from twitter_api.client.oauth_session.twitter_oauth2_real_session import (
            TwitterOAuth2RealSession,
        )

        session = TwitterOAuth2RealSession(
            lambda access_token: TwitterApiRealClient.from_oauth2_bearer_token(
                access_token
            ),
            client_id=client_id,
            client_secret=client_secret,
            callback_url=callback_url,
            scope=scope,
            event_hooks=event_hooks,
            limits=limits,
            mounts=mounts,
            proxies=proxies,
            timeout=timeout,
            transport=transport,
            verify=verify,
        )

        client: TwitterOAuth2AuthorizeClient[
            TwitterApiRealClient
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
        mounts: Optional[Mapping[str, httpx.BaseTransport]] = None,
        proxies: Optional[httpx.ProxiesTypes] = None,
        timeout: httpx.TimeoutTypes = httpx.DEFAULT_TIMEOUT_CONFIG,
        transport: Optional[httpx.BaseTransport] = None,
        verify: httpx.VerifyTypes = True,
    ):
        from twitter_api.client.oauth_flow.twitter_oauth2_access_token_client import (
            TwitterOAuth2AccessTokenClient,
        )
        from twitter_api.client.oauth_session.twitter_oauth2_real_session import (
            TwitterOAuth2RealSession,
        )

        from .twitter_api_real_client import TwitterApiRealClient

        session = TwitterOAuth2RealSession(
            lambda access_token: TwitterApiRealClient.from_oauth2_bearer_token(
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
            mounts=mounts,
            proxies=proxies,
            timeout=timeout,
            transport=transport,
            verify=verify,
        )

        client: TwitterOAuth2AccessTokenClient[
            TwitterApiRealClient
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
        mounts: Optional[Mapping[str, httpx.BaseTransport]] = None,
        proxies: Optional[httpx.ProxiesTypes] = None,
        timeout: httpx.TimeoutTypes = httpx.DEFAULT_TIMEOUT_CONFIG,
        transport: Optional[httpx.BaseTransport] = None,
        verify: httpx.VerifyTypes = True,
    ):
        return TwitterApiRealClient(
            RequestRealClient(
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
        mounts: Optional[Mapping[str, httpx.BaseTransport]] = None,
        proxies: Optional[httpx.ProxiesTypes] = None,
        timeout: httpx.TimeoutTypes = httpx.DEFAULT_TIMEOUT_CONFIG,
        transport: Optional[httpx.BaseTransport] = None,
        verify: httpx.VerifyTypes = True,
    ):
        from twitter_api.client.oauth_session.twitter_oauth1_real_session import (
            TwitterOAuth1RealSession,
        )

        session = TwitterOAuth1RealSession(
            lambda access_token, access_secret: TwitterApiRealClient.from_oauth1_app(
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
            mounts=mounts,
            proxies=proxies,
            timeout=timeout,
            transport=transport,
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
        mounts: Optional[Mapping[str, httpx.BaseTransport]] = None,
        proxies: Optional[httpx.ProxiesTypes] = None,
        timeout: httpx.TimeoutTypes = httpx.DEFAULT_TIMEOUT_CONFIG,
        transport: Optional[httpx.BaseTransport] = None,
        verify: httpx.VerifyTypes = True,
    ):
        from twitter_api.client.oauth_flow.twitter_oauth1_access_token_client import (
            TwitterOAuth1AccessTokenClient,
        )
        from twitter_api.client.oauth_session.twitter_oauth1_real_session import (
            TwitterOAuth1RealSession,
        )

        from .twitter_api_real_client import TwitterApiRealClient

        session = TwitterOAuth1RealSession(
            lambda access_token, access_secret: TwitterApiRealClient.from_oauth1_app(
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
            mounts=mounts,
            proxies=proxies,
            timeout=timeout,
            transport=transport,
            verify=verify,
        )

        return TwitterOAuth1AccessTokenClient(
            authorization_response_url=authorization_response_url,
            session=session,
        )

    def close(self) -> None:
        self._real_request_client.close()

    def __enter__(self) -> Self:
        self._real_request_client.__enter__()

        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        self._real_request_client.__exit__(exc_type, exc_value, traceback)
