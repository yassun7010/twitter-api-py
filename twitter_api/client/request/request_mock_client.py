from typing import Generic, Optional, Type, Union

from twitter_api.error import (
    MockInjectionResponseWrong,
    MockResponseNotFound,
    TwitterApiError,
)
from twitter_api.rate_limit.manager.no_operation_rate_limit_manager import (
    NoOperationRateLimitManager,
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


class RequestMockClient(RequestClient, Generic[ResponseModelBody]):
    def __init__(
        self,
        *,
        oauth_version: OAuthVersion,
        rate_limit_target: RateLimitTarget,
        rate_limit_manager: RateLimitManager,
    ):
        self._store: list[
            tuple[Endpoint, Union[ResponseModelBody, TwitterApiError]]
        ] = []
        self._oauth_version: OAuthVersion = oauth_version
        self._rate_limit_target: RateLimitTarget = rate_limit_target

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

    def inject_response_body(
        self,
        endpoint: Endpoint,
        response_body: Union[ResponseModelBody, TwitterApiError],
    ):
        self._store.append((endpoint, response_body))

    def _extract_response_body(self, endpoint: Endpoint) -> ResponseModelBody:
        if len(self._store) == 0:
            raise MockResponseNotFound()

        expected_endpoint, response_body = self._store.pop(0)

        if endpoint != expected_endpoint:
            raise MockInjectionResponseWrong(endpoint, expected_endpoint)

        if isinstance(response_body, TwitterApiError):
            raise response_body

        return response_body

    def get(
        self,
        *,
        endpoint: Endpoint,
        response_body_type: Type[ResponseModelBody],
        url: Optional[Url] = None,
        auth: bool = True,
        query: Optional[QuryParameters] = None,
    ) -> ResponseModelBody:
        return self._extract_response_body(endpoint)

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
        return self._extract_response_body(endpoint)

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
        return self._extract_response_body(endpoint)
