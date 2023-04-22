from twitter_api.client.request.async_request_client import AsyncRequestClient
from twitter_api.client.request.mock_request_client import MockRequestClient


class AsyncMockRequestClient(AsyncRequestClient, MockRequestClient):
    pass
