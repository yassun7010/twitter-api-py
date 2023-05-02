from typing import Mapping, Optional, Self, Type

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
from twitter_api.types import httpx
from twitter_api.types.endpoint import Endpoint
from twitter_api.types.http import Url
from twitter_api.types.oauth import OAuth, OAuthVersion

from .request_client import Headers, QuryParameters, RequestJsonBody, ResponseModelBody


class RequestAsyncRealClient(RequestAsyncClient):
    def __init__(
        self,
        *,
        auth: Optional[OAuth],
        oauth_version: OAuthVersion,
        rate_limit_target: RateLimitTarget,
        rate_limit_manager: RateLimitManager,
        event_hooks: Optional[Mapping[str, list[httpx.EventHook]]],
        limits: httpx.Limits,
        mounts: Optional[Mapping[str, httpx.AsyncBaseTransport]],
        proxies: Optional[httpx.ProxiesTypes],
        timeout: httpx.TimeoutTypes,
        transport: Optional[httpx.AsyncBaseTransport],
        verify: httpx.VerifyTypes,
        session: Optional[httpx.AsyncClient] = None,
    ) -> None:
        if session is None:
            session = httpx.AsyncClient(
                event_hooks=event_hooks,
                limits=limits,
                mounts=mounts,
                proxies=proxies,
                timeout=timeout,
                transport=transport,
                verify=verify,
            )

        self._oauth_version: OAuthVersion = oauth_version
        self._rate_limit_target: RateLimitTarget = rate_limit_target
        self._auth = auth
        self._session = session

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
        response_body_type: Type[ResponseModelBody],
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
        )

        return _parse_response(
            endpoint,
            response,
            response_body_type,
            url,
            headers,
            query,
            body,
        )

    async def post(
        self,
        *,
        endpoint: Endpoint,
        response_body_type: Type[ResponseModelBody],
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
        )

        return _parse_response(
            endpoint,
            response,
            response_body_type,
            url,
            headers,
            query,
            body,
        )

    async def delete(
        self,
        *,
        endpoint: Endpoint,
        response_body_type: Type[ResponseModelBody],
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
        )

        return _parse_response(
            endpoint,
            response,
            response_body_type,
            url,
            headers,
            query,
        )

    async def aclose(self) -> None:
        await self._session.aclose()

    async def __aenter__(self) -> Self:
        await self._session.__aenter__()
        return self

    async def __aexit__(self, exc_type, exc_value, traceback) -> None:
        await self._session.__aexit__(exc_type, exc_value, traceback)
