from typing import Any, Callable, Generic, Mapping, Optional

from authlib.integrations.httpx_client.oauth2_client import OAuth2Client

from twitter_api.client.oauth_session.resources.oauth2_authorize import (
    Oauth2AuthorizeUrl,
)
from twitter_api.client.oauth_session.resources.v2_oauth2_token import V2Oauth2TokenUrl
from twitter_api.client.oauth_session.twitter_oauth2_session import TwitterOAuth2Session
from twitter_api.types import httpx
from twitter_api.types._generic_client import TwitterApiGenericClient
from twitter_api.types.oauth import AccessToken, CallbackUrl, ClientId, ClientSecret
from twitter_api.types.oauth2.oauth2_access_token import OAuth2AccessToken
from twitter_api.types.oauth2.oauth2_authorization import OAuth2Authorization
from twitter_api.types.v2_scope import Scope
from twitter_api.utils._oauth import generate_code_verifier


class TwitterOAuth2RealSession(TwitterOAuth2Session, Generic[TwitterApiGenericClient]):
    def __init__(
        self,
        client_generator: Callable[[AccessToken], TwitterApiGenericClient],
        *,
        client_id: ClientId,
        client_secret: ClientSecret,
        callback_url: CallbackUrl,
        scope: Optional[list[Scope]],
        event_hooks: Optional[Mapping[str, list[httpx.EventHook]]],
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

    def generate_authorization_url(
        self,
    ) -> OAuth2Authorization[TwitterApiGenericClient]:
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
    ) -> OAuth2AccessToken[TwitterApiGenericClient]:
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
            _client_generator=self._client_generator,
            **response,
        )
