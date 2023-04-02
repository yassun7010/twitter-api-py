from typing import Optional, Type

import requests
from authlib.integrations.requests_client.oauth1_session import (
    OAuth1Auth,  # pyright: reportMissingImports=false
)
from authlib.integrations.requests_client.oauth2_session import (
    OAuth2Auth,  # pyright: reportMissingImports=false
)

from twitter_api.error import (
    TwitterApiOAuthTokenV1NotFound,
    TwitterApiResponseError,
    TwitterApiResponseFailed,
    TwitterApiResponseModelBodyDecodeError,
)
from twitter_api.ratelimit.ratelimit_target import RateLimitTarget
from twitter_api.types.endpoint import Endpoint
from twitter_api.types.http import Url
from twitter_api.types.oauth import OAuthVersion

from .request_client import (
    Headers,
    QuryParameters,
    RequestClient,
    RequestJsonBody,
    ResponseModelBody,
)

OAuth = OAuth2Auth | OAuth1Auth


class RealRequestClient(RequestClient):
    def __init__(
        self,
        *,
        oauth_version: OAuthVersion,
        rate_limit: RateLimitTarget,
        auth: Optional[OAuth],
        session: Optional[requests.Session] = None,
        timeout_sec: Optional[float] = None,
    ) -> None:
        if session is None:
            session = requests.Session()

        self._oauth_version: OAuthVersion = oauth_version
        self._rate_limit: RateLimitTarget = rate_limit
        self._auth = auth
        self._session = session
        self.timeout_sec = timeout_sec

    @property
    def oauth_version(self) -> OAuthVersion:
        return self._oauth_version

    @property
    def rate_limit(self) -> RateLimitTarget:
        return self._rate_limit

    def get(
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

        response = self._session.request(
            url=url,
            auth=self._auth if auth else None,
            method=endpoint.method,
            params=query,
            timeout=self.timeout_sec,
        )

        return response_type(
            **_parse_response(
                endpoint,
                response,
                url,
                headers,
                query,
                body,
            )
        )

    def post(
        self,
        *,
        endpoint: Endpoint,
        response_type: Type[ResponseModelBody],
        url: Optional[Url] = None,
        auth: bool = True,
        headers: Optional[Headers] = None,
        query: Optional[QuryParameters] = None,
        body: Optional[RequestJsonBody] = None,
        json: Optional[RequestJsonBody] = None,
    ) -> ResponseModelBody:
        url = endpoint.url if url is None else url

        response = self._session.request(
            url=url,
            auth=self._auth if auth else None,
            method=endpoint.method,
            headers=headers,
            params=query,
            data=body,
            json=json,
            timeout=self.timeout_sec,
        )

        if response_type is str:
            return response.content.decode("utf-8")  # type: ignore

        return response_type(
            **_parse_response(
                endpoint,
                response,
                url,
                headers,
                query,
                body,
            )
        )

    def delete(
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

        response = self._session.request(
            url=url,
            auth=self._auth if auth else None,
            method=endpoint.method,
            headers=headers,
            params=query,
            timeout=self.timeout_sec,
        )

        if response_type is str:
            return response.content.decode("utf-8")  # type: ignore

        return response_type(
            **_parse_response(
                endpoint,
                response,
                url,
                headers,
                query,
            )
        )


def _parse_response(
    endpoint: Endpoint,
    response: requests.Response,
    url: Url,
    headers: Optional[Headers] = None,
    query: Optional[QuryParameters] = None,
    body: Optional[RequestJsonBody] = None,
) -> dict:
    if response.content == b"":
        data: dict = {}
    else:
        try:
            data = response.json()
        except ValueError:
            if not response.ok:
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

    if not response.ok:
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

    return data
