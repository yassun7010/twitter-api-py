from typing import TypeVar

from twitter_api.client.twitter_api_async_client import TwitterApiAsyncClient
from twitter_api.client.twitter_api_async_mock_client import TwitterApiAsyncMockClient
from twitter_api.client.twitter_api_client import TwitterApiClient
from twitter_api.client.twitter_api_mock_client import TwitterApiMockClient

TwitterApiGenericClient = TypeVar(
    "TwitterApiGenericClient", TwitterApiClient, TwitterApiAsyncClient
)

TwitterApiGenericMockClient = TypeVar(
    "TwitterApiGenericMockClient", TwitterApiMockClient, TwitterApiAsyncMockClient
)
