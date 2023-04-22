from typing import Optional, Self, Type

import httpx
from authlib.integrations.httpx_client.oauth1_client import OAuth1Auth
from authlib.integrations.httpx_client.oauth2_client import OAuth2Auth

from twitter_api.client.request.request_async_client import RequestAsyncClient
from twitter_api.client.request.request_real_client import (
    _parse_response,
    _remove_none_field,
)
from twitter_api.rate_limit.manager.no_operation_rate_limit_manager import (
    NoOperationRateLimitManager,
)
from twitter_api.rate_limit.manager.rate_limit_manager import RateLimitManager
from twitter_api.rate_limit.rate_limit_target import RateLimitTarget
from twitter_api.types.endpoint import Endpoint
from twitter_api.types.http import Url
from twitter_api.types.oauth import OAuthVersion

from .request_client import Headers, QuryParameters, RequestJsonBody, ResponseModelBody

OAuth = OAuth2Auth | OAuth1Auth


class RequestAsyncRealClient(RequestAsyncClient):
    def __init__(
        self,
        *,
        auth: Optional[OAuth],
        oauth_version: OAuthVersion,
        rate_limit_target: RateLimitTarget,
        rate_limit_manager: Optional[RateLimitManager] = None,
        session: Optional[httpx.AsyncClient] = None,
        timeout_sec: Optional[float] = None,
    ) -> None:
        if session is None:
            session = httpx.AsyncClient()

        self._oauth_version: OAuthVersion = oauth_version
        self._rate_limit_target: RateLimitTarget = rate_limit_target
        self._auth = auth
        self._session = session
        self.timeout_sec = timeout_sec

        if rate_limit_manager is None:
            rate_limit_manager = NoOperationRateLimitManager()

        self._rate_limit_manager = rate_limit_manager

    @property
    def oauth_version(self) -> OAuthVersion:
        return self._oauth_version

    @property
    def rate_limit_target(self) -> RateLimitTarget:
        return self._rate_limit_target

    @property
    def rate_limit_manager(self) -> RateLimitManager:
        return self._rate_limit_manager

    async def get(
        self,
        *,
        endpoint: Endpoint,
        response_type: Type[ResponseModelBody],
        url: Optional[Url] = None,
        auth: bool = True,
        headers: Optional[Headers] = None,
        query: Optional[QuryParameters] = None,
        body: Optional[RequestJsonBody] = None,
    ) -> ResponseModelBody:
        url = endpoint.url if url is None else url

        response = await self._session.request(
            url=url,
            auth=self._auth if auth else None,
            method=endpoint.method,
            params=_remove_none_field(query),
            timeout=self.timeout_sec,
        )

        return _parse_response(
            endpoint,
            response,
            response_type,
            url,
            headers,
            query,
            body,
        )

    async def post(
        self,
        *,
        endpoint: Endpoint,
        response_type: Type[ResponseModelBody],
        url: Optional[Url] = None,
        auth: bool = True,
        headers: Optional[Headers] = None,
        query: Optional[QuryParameters] = None,
        body: Optional[RequestJsonBody] = None,
    ) -> ResponseModelBody:
        url = endpoint.url if url is None else url

        response = await self._session.request(
            url=url,
            auth=self._auth if auth else None,
            method=endpoint.method,
            headers=headers,
            params=_remove_none_field(query),
            json=_remove_none_field(body),
            timeout=self.timeout_sec,
        )

        if response_type is str:
            return response.content.decode("utf-8")  # type: ignore

        return _parse_response(
            endpoint,
            response,
            response_type,
            url,
            headers,
            query,
            body,
        )

    async def delete(
        self,
        *,
        endpoint: Endpoint,
        response_type: Type[ResponseModelBody],
        url: Optional[Url] = None,
        auth: bool = True,
        headers: Optional[Headers] = None,
        query: Optional[QuryParameters] = None,
    ) -> ResponseModelBody:
        url = endpoint.url if url is None else url

        response = await self._session.request(
            url=url,
            auth=self._auth if auth else None,
            method=endpoint.method,
            headers=headers,
            params=_remove_none_field(query),
            timeout=self.timeout_sec,
        )

        if response_type is str:
            return response.content.decode("utf-8")  # type: ignore

        return _parse_response(
            endpoint,
            response,
            response_type,
            url,
            headers,
            query,
        )

    async def __aenter__(self) -> Self:
        await self._session.__aenter__()
        return self

    async def __aexit__(self, exc_type, exc_value, traceback) -> None:
        await self._session.__aexit__(exc_type, exc_value, traceback)
