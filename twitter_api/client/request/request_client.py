from abc import ABCMeta, abstractmethod
from typing import Optional, Self, Type

from twitter_api.rate_limit.manager.rate_limit_manager import RateLimitManager
from twitter_api.rate_limit.rate_limit_target import RateLimitTarget
from twitter_api.types.endpoint import Endpoint
from twitter_api.types.http import (
    Headers,
    QuryParameters,
    RequestJsonBody,
    ResponseModelBody,
    Url,
)
from twitter_api.types.oauth import OAuthVersion


class RequestClient(metaclass=ABCMeta):
    @property
    @abstractmethod
    def oauth_version(self) -> OAuthVersion:
        ...

    @property
    @abstractmethod
    def rate_limit_target(self) -> RateLimitTarget:
        ...

    @property
    @abstractmethod
    def rate_limit_manager(self) -> RateLimitManager:
        ...

    @abstractmethod
    def get(
        self,
        *,
        endpoint: Endpoint,
        response_body_type: Type[ResponseModelBody],
        url: Optional[Url] = None,
        auth: bool = True,
        query: Optional[QuryParameters] = None,
    ) -> ResponseModelBody:
        ...

    @abstractmethod
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
        ...

    @abstractmethod
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
        ...

    def close(self) -> None:
        pass

    def __enter__(self) -> Self:
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        pass
