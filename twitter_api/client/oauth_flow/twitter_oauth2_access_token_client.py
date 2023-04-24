import os
from typing import Mapping, Optional

from twitter_api.client.oauth_session.resources.v2_oauth2_token import (
    V2OAuth2TokenRerources,
    V2Oauth2TokenUrl,
)
from twitter_api.client.oauth_session.twitter_oauth2_real_session import (
    TwitterOAuth2RealSession,
)
from twitter_api.client.oauth_session.twitter_oauth2_session import TwitterOAuth2Session
from twitter_api.rate_limit.manager import DEFAULT_RATE_LIMIT_MANAGER
from twitter_api.rate_limit.manager.rate_limit_manager import RateLimitManager
from twitter_api.types import httpx
from twitter_api.types.chainable import Chainable
from twitter_api.types.oauth import CallbackUrl, ClientId, ClientSecret, Env


class TwitterOAuth2AccessTokenClient(Chainable):
    def __init__(
        self,
        authorization_response_url: CallbackUrl,
        state: str,
        code_verifier: str,
        session: TwitterOAuth2Session,
    ):
        self.authorization_response_url = authorization_response_url
        self.state = state
        self.code_verifier = code_verifier
        self._session = session

    def resource(self, url: V2Oauth2TokenUrl):
        return V2OAuth2TokenRerources(
            authorization_response_url=self.authorization_response_url,
            state=self.state,
            code_verifier=self.code_verifier,
            session=self._session,
        )

    @classmethod
    def from_authorization_response_url(
        cls,
        *,
        client_id: ClientId,
        client_secret: ClientSecret,
        callback_url: CallbackUrl,
        authorization_response_url: CallbackUrl,
        state: str,
        code_verifier: str,
        rate_limit_manager: RateLimitManager = DEFAULT_RATE_LIMIT_MANAGER,
        event_hooks: Optional[httpx.EventHook] = None,
        limits: httpx.Limits = httpx.DEFAULT_LIMITS,
        mounts: Optional[Mapping[str, httpx.BaseTransport]] = None,
        proxies: Optional[httpx.ProxiesTypes] = None,
        timeout: httpx.TimeoutTypes = httpx.DEFAULT_TIMEOUT_CONFIG,
        transport: Optional[httpx.BaseTransport] = None,
        verify: httpx.VerifyTypes = True,
    ):
        session = TwitterOAuth2RealSession(
            client_id=client_id,
            client_secret=client_secret,
            callback_url=callback_url,
            scope=None,
            rate_limit_manager=rate_limit_manager,
            event_hooks=event_hooks,
            limits=limits,
            mounts=mounts,
            proxies=proxies,
            timeout=timeout,
            transport=transport,
            verify=verify,
        )

        return TwitterOAuth2AccessTokenClient(
            authorization_response_url=authorization_response_url,
            state=state,
            code_verifier=code_verifier,
            session=session,
        )

    @classmethod
    def from_authorization_response_url_env(
        cls,
        *,
        client_id_env: Env[ClientId] = "CLIENT_ID",
        client_secret_env: Env[ClientSecret] = "CLIENT_SECRET",
        callback_url_env: Env[CallbackUrl] = "CALLBACK_URL",
        authorization_response_url: CallbackUrl,
        state: str,
        code_verifier: str,
        callback_url: Optional[CallbackUrl] = None,
    ):
        return cls.from_authorization_response_url(
            client_id=cls._get_env(client_id_env),
            client_secret=cls._get_env(client_secret_env),
            callback_url=(
                cls._get_env(callback_url_env) if callback_url is None else callback_url
            ),
            authorization_response_url=authorization_response_url,
            state=state,
            code_verifier=code_verifier,
        )

    @classmethod
    def _get_env(cls, key: Env[str]) -> str:
        """環境変数を取り出す。"""
        return os.environ[key]
