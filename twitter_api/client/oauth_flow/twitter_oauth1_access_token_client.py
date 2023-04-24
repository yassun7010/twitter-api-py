import os
from typing import Mapping, Optional

from twitter_api.client.oauth_session.resources.oauth1_access_token import (
    Oauth1AccessTokenResources,
    Oauth1AccessTokenUrl,
)
from twitter_api.client.oauth_session.twitter_oauth1_real_session import (
    TwitterOAuth1RealSession,
)
from twitter_api.client.oauth_session.twitter_oauth1_session import TwitterOAuth1Session
from twitter_api.rate_limit.manager.rate_limit_manager import RateLimitManager
from twitter_api.types import httpx
from twitter_api.types.chainable import Chainable
from twitter_api.types.oauth import ApiKey, ApiSecret, CallbackUrl, Env


class TwitterOAuth1AccessTokenClient(Chainable):
    def __init__(
        self,
        authorization_response_url: CallbackUrl,
        session: TwitterOAuth1Session,
    ):
        self.authorization_response_url = authorization_response_url
        self._session = session

    def resource(self, url: Oauth1AccessTokenUrl):
        return Oauth1AccessTokenResources(
            session=self._session,
            authorization_response_url=self.authorization_response_url,
        )

    @classmethod
    def from_authorization_response_url(
        cls,
        *,
        api_key: ApiKey,
        api_secret: ApiSecret,
        callback_url: CallbackUrl,
        authorization_response_url: CallbackUrl,
        rate_limit_manager: Optional[RateLimitManager] = None,
        event_hooks: Optional[httpx.EventHook] = None,
        limits: Optional[httpx.Limits] = None,
        mounts: Optional[Mapping[str, httpx.BaseTransport]] = None,
        proxies: Optional[httpx.ProxiesTypes] = None,
        timeout: Optional[httpx.TimeoutTypes] = None,
        transport: Optional[httpx.BaseTransport] = None,
        verify: Optional[httpx.VerifyTypes] = None,
    ):
        session = TwitterOAuth1RealSession(
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

        return TwitterOAuth1AccessTokenClient(
            authorization_response_url=authorization_response_url,
            session=session,
        )

    @classmethod
    def from_authorization_response_url_env(
        cls,
        *,
        api_key_env: Env[ApiKey] = "API_KEY",
        api_secret_env: Env[ApiSecret] = "API_SECRET",
        callback_url_env: Env[CallbackUrl] = "CALLBACK_URL",
        authorization_response_url: CallbackUrl,
        callback_url: Optional[CallbackUrl] = None,
    ):
        return cls.from_authorization_response_url(
            api_key=cls._get_env(api_key_env),
            api_secret=cls._get_env(api_secret_env),
            callback_url=(
                cls._get_env(callback_url_env) if callback_url is None else callback_url
            ),
            authorization_response_url=authorization_response_url,
        )

    @classmethod
    def _get_env(cls, key: Env[str]) -> str:
        """環境変数を取り出す。"""
        return os.environ[key]
