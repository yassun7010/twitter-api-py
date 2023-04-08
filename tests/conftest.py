import os

import pytest

from tests.data import JsonDataLoader
from twitter_api.client.twitter_api_mock_client import TwitterApiMockClient
from twitter_api.client.twitter_api_real_client import TwitterApiRealClient


def synthetic_monitoring_is_disable() -> dict:
    """
    外形監視が無効であるかどうかを確認する。

    下記の環境変数を設定すると、実際に API を叩いてテストが行われる。

    ```env
    SYNTHETIC_MONITORING_TEST=true
    ```
    """

    return dict(
        condition=(
            "SYNTHETIC_MONITORING_TEST" not in os.environ
            or os.environ["SYNTHETIC_MONITORING_TEST"].lower() != "true"
        ),
        reason="外形監視が有効時（環境変数 SYNTHETIC_MONITORING_TEST が true ）に実行されます。",
    )


@pytest.fixture
def json_data_loader() -> JsonDataLoader:
    return JsonDataLoader()


@pytest.fixture
def real_app_auth_v2_client() -> TwitterApiRealClient:
    return TwitterApiRealClient.from_app_oauth2_env()


@pytest.fixture
def real_user_auth_v2_client() -> TwitterApiRealClient:
    return (
        TwitterApiRealClient.from_user_oauth2_flow_env()
        .request("https://twitter.com/i/oauth2/authorize")
        .open_authorization_url()
        .input_authorization_response_url()
        .request("https://api.twitter.com/2/oauth2/token")
        .post()
        .generate_client()
    )


@pytest.fixture
def real_user_auth_v1_client() -> TwitterApiRealClient:
    return TwitterApiRealClient.from_user_oauth1_env()


@pytest.fixture
def mock_app_auth_v2_client() -> TwitterApiMockClient:
    return TwitterApiMockClient(
        oauth_version="2.0",
        rate_limit_target="app",
    )


@pytest.fixture
def mock_user_auth_v2_client() -> TwitterApiMockClient:
    return TwitterApiMockClient(
        oauth_version="2.0",
        rate_limit_target="user",
    )


@pytest.fixture
def mock_app_auth_v1_client() -> TwitterApiMockClient:
    return TwitterApiMockClient(
        oauth_version="1.0a",
        rate_limit_target="app",
    )


@pytest.fixture
def mock_user_auth_v1_client() -> TwitterApiMockClient:
    return TwitterApiMockClient(
        oauth_version="1.0a",
        rate_limit_target="user",
    )
