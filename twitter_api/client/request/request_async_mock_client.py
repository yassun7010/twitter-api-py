from typing_extensions import Self

from twitter_api.client.request.request_async_client import RequestAsyncClient
from twitter_api.client.request.request_mock_client import _RequestMockClient


class RequestAsyncMockClient(_RequestMockClient, RequestAsyncClient):
    async def aclose(self) -> None:
        pass

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(self, exc_type, exc_value, traceback) -> None:
        pass
