import pytest

from twitter_api.client.twitter_api_client import TwitterApiClient
from twitter_api.client.twitter_api_mock_client import TwitterApiMockClient
from twitter_api.client.twitter_api_real_client import TwitterApiRealClient


@pytest.fixture
def client() -> TwitterApiClient:
    return TwitterApiClient.from_app_auth_env()


@pytest.fixture
def real_client() -> TwitterApiRealClient:
    return TwitterApiRealClient.from_app_auth_env()


@pytest.fixture
def mock_client() -> TwitterApiMockClient:
    return TwitterApiMockClient()
