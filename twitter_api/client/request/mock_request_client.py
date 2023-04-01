from typing import Generic, Optional, Type

from twitter_api.error import MockInjectionResponseWrong, MockResponseNotFound
from twitter_api.types.endpoint import Endpoint

from .request_client import (
    Headers,
    QuryParameters,
    RequestClient,
    RequestJsonBody,
    ResponseModelBody,
)


class MockRequestClient(RequestClient, Generic[ResponseModelBody]):
    def __init__(self):
        self._store: list[tuple[Endpoint, ResponseModelBody]] = []

    def inject_response_body(
        self, endpoint: Endpoint, response: ResponseModelBody
    ):
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
        uri: Optional[str] = None,
        query: Optional[QuryParameters] = None,
    ) -> ResponseModelBody:
        return self.extract_response_body(endpoint)

    def post(
        self,
        *,
        endpoint: Endpoint,
        response_type: Type[ResponseModelBody],
        uri: Optional[str] = None,
        headers: Optional[Headers] = None,
        query: Optional[QuryParameters] = None,
        body: Optional[RequestJsonBody] = None,
    ) -> ResponseModelBody:
        return self.extract_response_body(endpoint)
