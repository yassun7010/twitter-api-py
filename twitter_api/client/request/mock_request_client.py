from typing import Generic, Optional, Type

from twitter_api.error import MockInjectionResponseWrong, MockResponseNotFound
from twitter_api.ratelimit.ratelimit_target import RatelimitTarget
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


class MockRequestClient(RequestClient, Generic[ResponseModelBody]):
    def __init__(
        self,
        *,
        rate_limit: RatelimitTarget,
        oauth_version: OAuthVersion,
    ):
        self._store: list[tuple[Endpoint, ResponseModelBody]] = []
        self._rate_limit: RatelimitTarget = rate_limit
        self._oauth_version: OAuthVersion = oauth_version

    @property
    def oauth_version(self) -> OAuthVersion:
        return self._oauth_version

    @property
    def rate_limit(self) -> RatelimitTarget:
        return self._rate_limit

    def inject_response_body(self, endpoint: Endpoint, response: ResponseModelBody):
        self._store.append((endpoint, response))

    def extract_response_body(self, endpoint: Endpoint) -> ResponseModelBody:
        if len(self._store) == 0:
            raise MockResponseNotFound()

        expected_endpoint, response = self._store.pop(0)

        if endpoint != expected_endpoint:
            raise MockInjectionResponseWrong(endpoint, expected_endpoint)

        return response

    def get(
        self,
        *,
        endpoint: Endpoint,
        response_type: Type[ResponseModelBody],
        url: Optional[Url] = None,
        auth: bool = True,
        query: Optional[QuryParameters] = None,
    ) -> ResponseModelBody:
        return self.extract_response_body(endpoint)

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
        return self.extract_response_body(endpoint)

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
        return self.extract_response_body(endpoint)
