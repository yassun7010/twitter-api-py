from typing import Mapping, Optional, Self, Type

import pydantic
from authlib.integrations.httpx_client.oauth1_client import OAuth1Auth
from authlib.integrations.httpx_client.oauth2_client import OAuth2Auth

from twitter_api.error import (
    TwitterApiOAuthTokenV1NotFound,
    TwitterApiResponseError,
    TwitterApiResponseFailed,
    TwitterApiResponseModelBodyDecodeError,
    TwitterApiResponseValidationError,
)
from twitter_api.rate_limit.manager.no_operation_rate_limit_manager import (
    NoOperationRateLimitManager,
)
from twitter_api.rate_limit.manager.rate_limit_manager import RateLimitManager
from twitter_api.rate_limit.rate_limit_target import RateLimitTarget
from twitter_api.types.endpoint import Endpoint
from twitter_api.types.http import Url
from twitter_api.types.oauth import OAuthVersion
from twitter_api.utils import httpx

from .request_client import (
    Headers,
    QuryParameters,
    RequestClient,
    RequestJsonBody,
    ResponseModelBody,
)

OAuth = OAuth2Auth | OAuth1Auth


class RequestRealClient(RequestClient):
    def __init__(
        self,
        *,
        auth: Optional[OAuth],
        oauth_version: OAuthVersion,
        rate_limit_target: RateLimitTarget,
        rate_limit_manager: Optional[RateLimitManager],
        event_hooks: Optional[httpx.EventHook],
        limits: Optional[httpx.Limits],
        mounts: Optional[Mapping[str, httpx.BaseTransport]],
        proxies: Optional[httpx.ProxiesTypes],
        timeout: Optional[httpx.TimeoutTypes],
        transport: Optional[httpx.BaseTransport],
        verify: Optional[httpx.VerifyTypes],
        session: Optional[httpx.Client] = None,
        **httpx_client_kwargs,
    ) -> None:
        if session is None:
            session = httpx.Client(
                **httpx.update_client_kwargs(
                    event_hooks,
                    limits,
                    mounts,
                    proxies,
                    timeout,
                    transport,
                    verify,
                    kwargs=httpx_client_kwargs,
                )
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

    def get(
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

        response = self._session.request(
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

    def post(
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

        response = self._session.request(
            url=url,
            auth=self._auth if auth else None,
            method=endpoint.method,
            headers=headers,
            params=_remove_none_field(query),
            json=_remove_none_field(body),
        )

        if response_body_type is str:
            return response.content.decode("utf-8")  # type: ignore

        return _parse_response(
            endpoint,
            response,
            response_body_type,
            url,
            headers,
            query,
            body,
        )

    def delete(
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

        response = self._session.request(
            url=url,
            auth=self._auth if auth else None,
            method=endpoint.method,
            headers=headers,
            params=_remove_none_field(query),
        )

        if response_body_type is str:
            return response.content.decode("utf-8")  # type: ignore

        return _parse_response(
            endpoint,
            response,
            response_body_type,
            url,
            headers,
            query,
        )

    def close(self) -> None:
        self._session.close()

    def __enter__(self) -> Self:
        self._session = self._session.__enter__()

        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        self._session.__exit__(exc_type, exc_value, traceback)


def _parse_response(
    endpoint: Endpoint,
    response: httpx.Response,
    response_body_type: Type[ResponseModelBody],
    url: Url,
    headers: Optional[Headers] = None,
    query: Optional[QuryParameters] = None,
    body: Optional[RequestJsonBody] = None,
) -> ResponseModelBody:
    if response.content == b"":
        data: dict = {}
    else:
        try:
            data = response.json()
        except ValueError:
            if response.is_error:
                raise TwitterApiResponseFailed(
                    endpoint,
                    url=url,
                    request_headers=headers,
                    query=query,
                    request_body=body if body is not None else None,
                    response_status_code=response.status_code,
                    response_body=response.content,
                )
            else:
                raise TwitterApiResponseModelBodyDecodeError(
                    endpoint,
                    response.content,
                )

    if response.is_error:
        raise TwitterApiResponseFailed(
            endpoint,
            url=url,
            request_headers=headers,
            query=query,
            request_body=body if body is not None else None,
            response_status_code=response.status_code,
            response_body=data,
        )

    # If only errors will raise
    if "errors" in data and len(data.keys()) == 1:
        raise TwitterApiResponseError(
            endpoint,
            data,
        )

    # v1 token not
    if "reason" in data:
        raise TwitterApiOAuthTokenV1NotFound(
            endpoint,
            data,
        )

    try:
        return response_body_type(**data)
    except pydantic.ValidationError as error:
        raise TwitterApiResponseValidationError(endpoint, data, error)


def _remove_none_field(data: Optional[dict]) -> Optional[dict]:
    if data is None:
        return None

    return {
        k: _remove_none_field(v) if isinstance(v, dict) else v
        for k, v in data.items()
        if v is not None
    }
