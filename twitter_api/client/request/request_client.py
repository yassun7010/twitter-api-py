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


class RequestClient(metaclass=ABCMeta):
    @property
    @abstractmethod
    def oauth_version(self) -> OAuthVersion:
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
    ) -> ResponseModelBody:
        ...
