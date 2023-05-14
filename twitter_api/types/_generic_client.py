from typing import TypeVar

from twitter_api.client.twitter_api_async_client import TwitterApiAsyncClient
from twitter_api.client.twitter_api_async_mock_client import TwitterApiAsyncMockClient
from twitter_api.client.twitter_api_async_real_client import TwitterApiAsyncRealClient
from twitter_api.client.twitter_api_client import TwitterApiClient
from twitter_api.client.twitter_api_mock_client import TwitterApiMockClient
from twitter_api.client.twitter_api_real_client import TwitterApiRealClient

TwitterApiGenericClient = TypeVar(
    "TwitterApiGenericClient", TwitterApiClient, TwitterApiAsyncClient
)

TwitterApiGenericRealClient = TypeVar(
    "TwitterApiGenericRealClient", TwitterApiRealClient, TwitterApiAsyncRealClient
)

TwitterApiGenericMockClient = TypeVar(
    "TwitterApiGenericMockClient", TwitterApiMockClient, TwitterApiAsyncMockClient
)
