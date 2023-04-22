from twitter_api.client.request.request_async_client import RequestAsyncClient
from twitter_api.client.request.request_mock_client import RequestMockClient


class RequestAsyncMockClient(RequestAsyncClient, RequestMockClient):
    pass
