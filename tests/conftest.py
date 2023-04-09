import os
from contextlib import contextmanager

import pytest

from tests.data import JsonDataLoader
from twitter_api.api.types.v2_user.user_id import UserId
from twitter_api.client.twitter_api_mock_client import TwitterApiMockClient
from twitter_api.client.twitter_api_real_client import TwitterApiRealClient
from twitter_api.error import (
    OAuth2UserAccessTokenExpired,
    TwitterApiErrorCode,
    TwitterApiResponseFailed,
)


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


def premium_account_not_set() -> dict:
    """
    プレミアムアカウントの Access Token が未設定かを確認する。

    下記の環境変数を設定すると、テストが行われる。

    ```env
    OAUTH2_PREMIUM_ACCESS_TOKEN=XXXXXXXXXXXXXXXXXXXXXXX
    ```
    """

    return dict(
        condition=(
            "OAUTH2_PREMIUM_ACCESS_TOKEN" not in os.environ
            or os.environ["OAUTH2_PREMIUM_ACCESS_TOKEN"] == ""
        ),
        reason="プレミアムアカウントを持っている場合に実行されます。",
    )


@pytest.fixture
def json_data_loader() -> JsonDataLoader:
    return JsonDataLoader()


@pytest.fixture
def user_id() -> UserId:
    return os.environ["USER_ID"]


@pytest.fixture
def participant_id(user_id) -> UserId:
    """
    DM への参加者の ID。

    会話を作れるのはアプリ側なのでアプリ側のユーザ ID を用いる。
    """

    return user_id


@pytest.fixture
def participant_ids(participant_id: UserId) -> list[UserId]:
    """
    DM の会話への参加者たちの ID。

    """

    return [participant_id] + os.environ["PARTICIPANT_IDS"].split(",")


@pytest.fixture
def real_oauth2_bearer_client() -> TwitterApiRealClient:
    return TwitterApiRealClient.from_oauth2_bearer_token_env()


@pytest.fixture
def real_oauth2_app_client() -> TwitterApiRealClient:
    return TwitterApiRealClient.from_oauth2_app_env()


@pytest.fixture
def real_oauth2_user_client() -> TwitterApiRealClient:
    return TwitterApiRealClient.from_oauth2_bearer_token_env("OAUTH2_USER_ACCESS_TOKEN")


@pytest.fixture
def real_oauth1_user_client() -> TwitterApiRealClient:
    return TwitterApiRealClient.from_oauth1_user_env()


@pytest.fixture
def mock_oauth2_app_client() -> TwitterApiMockClient:
    return TwitterApiMockClient(
        oauth_version="2.0",
        rate_limit_target="app",
    )


@pytest.fixture
def mock_oauth2_user_client() -> TwitterApiMockClient:
    return TwitterApiMockClient(
        oauth_version="2.0",
        rate_limit_target="user",
    )


@pytest.fixture
def mock_oauth1_app_client() -> TwitterApiMockClient:
    return TwitterApiMockClient(
        oauth_version="1.0a",
        rate_limit_target="app",
    )


@pytest.fixture
def mock_oauth1_user_client() -> TwitterApiMockClient:
    return TwitterApiMockClient(
        oauth_version="1.0a",
        rate_limit_target="user",
    )


@contextmanager
def check_oauth2_user_access_token():
    """
    OAuth 2.0 のユーザ認証が失効することで自動テストが失敗することがある。

    ユーザ認証が失効することによってエラーが発生していることが分かるようにエラーを上書きする。
    """

    try:
        yield
    except TwitterApiResponseFailed as error:
        if error.status_code == TwitterApiErrorCode.Forbidden:
            raise OAuth2UserAccessTokenExpired()
        else:
            raise error
