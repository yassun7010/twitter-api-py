from abc import abstractmethod
from typing import Generic, Optional, Type

from twitter_api.types.endpoint import Endpoint
from twitter_api.types.http import (
    Headers,
    QuryParameters,
    RequestModelBody,
    ResponseModelBody,
)


class RequestClient(Generic[QuryParameters, ResponseModelBody]):
    @abstractmethod
    def get(
        self,
        *,
        endpoint: Endpoint,
        response_type: Type[ResponseModelBody],
        uri: Optional[str] = None,
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
        headers: Optional[Headers] = None,
        query: Optional[QuryParameters] = None,
        body: Optional[RequestModelBody] = None,
    ) -> ResponseModelBody:
        ...
