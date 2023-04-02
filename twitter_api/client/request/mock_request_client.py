from typing import Generic, Optional, Type

from twitter_api.error import MockInjectionResponseWrong, MockResponseNotFound
from twitter_api.rate_limit.manager.ignored_rate_limit_manager import (
    IgnoredRateLimitManager,
)
from twitter_api.rate_limit.manager.rate_limit_manager import RateLimitManager
from twitter_api.rate_limit.rate_limit_target import RateLimitTarget
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
        oauth_version: OAuthVersion,
        rate_limit_target: RateLimitTarget,
        rate_limit_manager: Optional[RateLimitManager] = None,
    ):
        self._store: list[tuple[Endpoint, ResponseModelBody]] = []
        self._oauth_version: OAuthVersion = oauth_version
        self._rate_limit_target: RateLimitTarget = rate_limit_target

        if rate_limit_manager is None:
            rate_limit_manager = IgnoredRateLimitManager()

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
