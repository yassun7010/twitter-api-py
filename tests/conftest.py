import pytest

from twitter_api.client.twitter_api_client import TwitterApiClient
from twitter_api.client.twitter_api_mock_client import TwitterApiMockClient
from twitter_api.client.twitter_api_real_client import TwitterApiRealClient


@pytest.fixture
def client():
    return TwitterApiClient.from_bearer_token("aaaaa")


@pytest.fixture
def real_client():
    return TwitterApiRealClient.from_bearer_token("aaaaa")


@pytest.fixture
def mock_client():
    return TwitterApiMockClient()
