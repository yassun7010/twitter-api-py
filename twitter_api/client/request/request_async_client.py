from abc import abstractmethod
from typing import Optional, Type

from twitter_api.client.request.request_client import RequestClient
from twitter_api.types.endpoint import Endpoint
from twitter_api.types.http import (
    Headers,
    QuryParameters,
    RequestJsonBody,
    ResponseModelBody,
    Url,
)


class RequestAsyncClient(RequestClient):
    @abstractmethod
    async def get(
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
        ...

    @abstractmethod
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
        ...
