from abc import ABCMeta, abstractmethod
from typing import Optional, Type

from twitter_api.types.endpoint import Endpoint
from twitter_api.types.http import (
    Headers,
    QuryParameters,
    RequestJsonBody,
    ResponseModelBody,
)
from twitter_api.types.oauth import OAuthVersion
from twitter_api.utils.ratelimit import RateLimitTarget


class RequestClient(metaclass=ABCMeta):
    @property
    @abstractmethod
    def oauth_version(self) -> OAuthVersion:
        ...

    @property
    @abstractmethod
    def rate_limit(self) -> RateLimitTarget:
        ...

    @abstractmethod
    def get(
        self,
        *,
        endpoint: Endpoint,
        response_type: Type[ResponseModelBody],
        uri: Optional[str] = None,
        auth: bool = True,
        query: Optional[QuryParameters] = None,
    ) -> ResponseModelBody:
        ...

    @abstractmethod
    def post(
        self,
        *,
        endpoint: Endpoint,
        response_type: Type[ResponseModelBody],
        uri: Optional[str] = None,
        auth: bool = True,
        headers: Optional[Headers] = None,
        query: Optional[QuryParameters] = None,
        body: Optional[RequestJsonBody] = None,
        json: Optional[RequestJsonBody] = None,
    ) -> ResponseModelBody:
        ...

    @abstractmethod
    def delete(
        self,
        *,
        endpoint: Endpoint,
        response_type: Type[ResponseModelBody],
        uri: Optional[str] = None,
        auth: bool = True,
        headers: Optional[Headers] = None,
        query: Optional[QuryParameters] = None,
    ) -> ResponseModelBody:
        ...
