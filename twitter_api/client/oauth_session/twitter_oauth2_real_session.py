from typing import Any, Callable, Generic, Mapping, Optional, Type, TypeVar

from authlib.integrations.httpx_client.oauth2_client import OAuth2Client

from twitter_api.api.types.oauth2.oauth2_access_token import OAuth2AccessToken
from twitter_api.api.types.oauth2.oauth2_authorization import OAuth2Authorization
from twitter_api.api.types.v2_scope import Scope
from twitter_api.client.oauth_session.resources.oauth2_authorize import (
    Oauth2AuthorizeUrl,
)
from twitter_api.client.oauth_session.resources.v2_oauth2_token import V2Oauth2TokenUrl
from twitter_api.client.oauth_session.twitter_oauth2_session import TwitterOAuth2Session
from twitter_api.client.twitter_api_async_client import TwitterApiAsyncClient
from twitter_api.client.twitter_api_async_real_client import TwitterApiAsyncRealClient
from twitter_api.client.twitter_api_client import TwitterApiClient
from twitter_api.client.twitter_api_real_client import TwitterApiRealClient
from twitter_api.rate_limit.manager.rate_limit_manager import RateLimitManager
from twitter_api.types import httpx
from twitter_api.types.oauth import CallbackUrl, ClientId, ClientSecret
from twitter_api.utils._oauth import generate_code_verifier

Client = TypeVar("Client", TwitterApiRealClient, TwitterApiAsyncRealClient)


class TwitterOAuth2RealSession(TwitterOAuth2Session, Generic[Client]):
    def __init__(
        self,
        client_generator: Callable[[str], Client],
        *,
        client_id: ClientId,
        client_secret: ClientSecret,
        callback_url: CallbackUrl,
        scope: Optional[list[Scope]],
        event_hooks: Optional[httpx.EventHook],
        limits: httpx.Limits,
        mounts: Optional[Mapping[str, httpx.BaseTransport]],
        proxies: Optional[httpx.ProxiesTypes],
        timeout: httpx.TimeoutTypes,
        transport: Optional[httpx.BaseTransport],
        verify: httpx.VerifyTypes,
    ) -> None:
        self._client_generator = client_generator
        self._session = OAuth2Client(
            client_id=client_id,
            client_secret=client_secret,
            redirect_uri=callback_url,
            scope=scope,
            code_challenge_method="S256",
            event_hooks=event_hooks,
            limits=limits,
            mounts=mounts,
            proxies=proxies,
            timeout=timeout,
            transport=transport,
            verify=verify,
        )

    def generate_authorization_url(self) -> OAuth2Authorization:
        url: Oauth2AuthorizeUrl = "https://twitter.com/i/oauth2/authorize"
        code_verifier = generate_code_verifier()

        authorization_url, state = self._session.create_authorization_url(
            url, code_verifier=code_verifier
        )

        return OAuth2Authorization(
            authorization_url=authorization_url,
            state=state,
            code_verifier=code_verifier,
            session=self,
        )

    def fetch_token(
        self,
        authorization_response_url: CallbackUrl,
        state: str,
        code_verifier: str,
    ) -> OAuth2AccessToken:
        url: V2Oauth2TokenUrl = "https://api.twitter.com/2/oauth2/token"

        response = self._session.fetch_token(
            url=url,
            authorization_response=authorization_response_url,
            state=state,
            code_verifier=code_verifier,
        )

        scope: Any = response.pop("scope", "").split(" ")

        # 認証のプロセスがすべて終了したので、コネクションを閉じておく。
        self._session.close()

        return OAuth2AccessToken(
            scope=scope,
            _session=self,
            **response,
        )

    def generate_client(self, access_token: str) -> Client:
        return self._client_generator(access_token)
