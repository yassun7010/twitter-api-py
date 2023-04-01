import os
from textwrap import dedent

import pytest

from twitter_api.client.twitter_api_client import TwitterApiClient
from twitter_api.client.twitter_api_mock_client import TwitterApiMockClient
from twitter_api.client.twitter_api_real_client import TwitterApiRealClient


def synthetic_monitoring_is_disable() -> dict:
    """
    外形監視が無効であるかどうかを確認する。

    下記の環境変数を設定すると、実際に API を叩いてテストが行われる。

    ```env
    SYNTHETIC_MONITORING=true
    ```
    """

    return dict(
        condition=(
            "SYNTHETIC_MONITORING" not in os.environ
            or os.environ["SYNTHETIC_MONITORING"].lower() != "true"
        ),
        reason=dedent(
            """
            環境変数 SYNTHETIC_MONITORING が true ではないため。
            実際に API を叩いて応答を確認したい場合のみ有効にする。
            """
        ).replace("\n", ""),
    )


@pytest.fixture
def client() -> TwitterApiClient:
    return TwitterApiClient.from_app_auth_env()


@pytest.fixture
def real_client() -> TwitterApiRealClient:
    return TwitterApiRealClient.from_app_auth_env()


@pytest.fixture
def mock_client() -> TwitterApiMockClient:
    return TwitterApiMockClient()
