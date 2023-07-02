import os
from textwrap import dedent

import pytest

from twitter_api.client.twitter_api_async_mock_client import TwitterApiAsyncMockClient
from twitter_api.client.twitter_api_async_real_client import TwitterApiAsyncRealClient
from twitter_api.client.twitter_api_mock_client import TwitterApiMockClient
from twitter_api.client.twitter_api_real_client import TwitterApiRealClient
from twitter_api.error import TwitterApiException
from twitter_api.types.v2_scope import ALL_SCOPES
from twitter_api.types.v2_tweet.tweet import Tweet
from twitter_api.types.v2_user.user import User
from twitter_api.types.v2_user.user_id import UserId


class PytestTwitterApiException(TwitterApiException):
    """
    Pytest で発生した TwitterAPI の例外は詳細な情報としてログに出したい。
    そのため、ログのフォーマットを詳細に変換するエラークラスを用意。
    """

    def __init__(self, error: TwitterApiException):
        self._error = error

    def __str__(self) -> str:
        return str(self._error.info.model_dump_json(indent=2))


def pytest_runtest_call(item: pytest.Item):
    try:
        item.runtest()
    except TwitterApiException as error:
        raise PytestTwitterApiException(error) from error


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
def user_id() -> UserId:
    """
    アプリ所有者か、承認を得たユーザの UserId 。

    自動テストでは、簡単のためアプリ所有者。
    """

    return os.environ["USER_ID"]


@pytest.fixture
def participant_id(user_id: UserId) -> UserId:
    """
    DM への参加者の UserId。

    会話を作れるのはアプリ所有者なので、アプリ所有者の UserId を用いる。
    """

    return user_id


@pytest.fixture
def participant_ids(participant_id: UserId) -> list[UserId]:
    """
    DM のグループ会話への参加者たちの UserId。

    グループを作る際、最低 2 人の参加が必要なので、アプリ所有者以外の UserId が必要になる。
    """

    return [participant_id] + os.environ["PARTICIPANT_IDS"].split(",")


@pytest.fixture
def oauth2_bearer_real_client() -> TwitterApiRealClient:
    return TwitterApiRealClient.from_oauth2_bearer_token_env()


@pytest.fixture
def oauth2_app_real_client() -> TwitterApiRealClient:
    return TwitterApiRealClient.from_oauth2_app_env()


@pytest.fixture
def oauth2_user_real_client() -> TwitterApiRealClient:
    return TwitterApiRealClient.from_oauth2_bearer_token_env("OAUTH2_USER_ACCESS_TOKEN")


@pytest.fixture
def oauth1_app_real_client() -> TwitterApiRealClient:
    return TwitterApiRealClient.from_oauth1_app_env()


@pytest.fixture
def oauth1_user_real_client() -> TwitterApiRealClient:
    return TwitterApiRealClient.from_oauth1_app_env(
        access_token_env="OAUTH1_USER_ACCESS_TOKEN",
        access_secret_env="OAUTH1_USER_ACCESS_SECRET",
    )


@pytest.fixture
def oauth2_bearer_async_real_client() -> TwitterApiAsyncRealClient:
    return TwitterApiAsyncRealClient.from_oauth2_bearer_token_env()


@pytest.fixture
def oauth2_app_async_real_client() -> TwitterApiAsyncRealClient:
    return TwitterApiAsyncRealClient.from_oauth2_app_env()


@pytest.fixture
def oauth2_user_async_real_client() -> TwitterApiAsyncRealClient:
    return TwitterApiAsyncRealClient.from_oauth2_bearer_token_env(
        "OAUTH2_USER_ACCESS_TOKEN"
    )


@pytest.fixture
def oauth1_app_async_real_client() -> TwitterApiAsyncRealClient:
    return TwitterApiAsyncRealClient.from_oauth1_app_env()


@pytest.fixture
def oauth1_user_async_real_client() -> TwitterApiAsyncRealClient:
    return TwitterApiAsyncRealClient.from_oauth1_app_env(
        access_token_env="OAUTH1_USER_ACCESS_TOKEN",
        access_secret_env="OAUTH1_USER_ACCESS_SECRET",
    )


@pytest.fixture
def oauth2_app_mock_client() -> TwitterApiMockClient:
    return TwitterApiMockClient.from_oauth2_app_env()


@pytest.fixture
def oauth2_user_mock_client() -> TwitterApiMockClient:
    return (
        TwitterApiMockClient.from_oauth2_user_flow_env(scope=ALL_SCOPES)
        .request("https://twitter.com/i/oauth2/authorize")
        .generate_authorization_url()
        .input_response_url("https://localhost:3000")
        .request("https://api.twitter.com/2/oauth2/token")
        .post()
        .generate_client()
    )


@pytest.fixture
def oauth1_app_mock_client() -> TwitterApiMockClient:
    return TwitterApiMockClient.from_oauth1_app_env()


@pytest.fixture
def oauth1_user_mock_client() -> TwitterApiMockClient:
    return (
        TwitterApiMockClient.from_oauth1_user_flow_env()
        .request("https://api.twitter.com/oauth/request_token")
        .post()
        .request("https://api.twitter.com/oauth/authorize")
        .generate_authorization_url()
        .input_response_url("https://localhost:3000")
        .request("https://api.twitter.com/oauth/access_token")
        .post()
        .generate_client()
    )


@pytest.fixture
def oauth2_app_async_mock_client() -> TwitterApiAsyncMockClient:
    return TwitterApiAsyncMockClient.from_oauth2_app_env()


@pytest.fixture
def oauth2_user_async_mock_client() -> TwitterApiAsyncMockClient:
    return (
        TwitterApiAsyncMockClient.from_oauth2_user_flow_env(scope=ALL_SCOPES)
        .request("https://twitter.com/i/oauth2/authorize")
        .generate_authorization_url()
        .input_response_url("https://localhost:3000")
        .request("https://api.twitter.com/2/oauth2/token")
        .post()
        .generate_client()
    )


@pytest.fixture
def oauth1_app_async_mock_client() -> TwitterApiAsyncMockClient:
    return TwitterApiAsyncMockClient.from_oauth1_app_env()


@pytest.fixture
def oauth1_user_async_mock_client() -> TwitterApiAsyncMockClient:
    return (
        TwitterApiAsyncMockClient.from_oauth1_user_flow_env()
        .request("https://api.twitter.com/oauth/request_token")
        .post()
        .request("https://api.twitter.com/oauth/authorize")
        .generate_authorization_url()
        .input_response_url("https://localhost:3000")
        .request("https://api.twitter.com/oauth/access_token")
        .post()
        .generate_client()
    )


@pytest.fixture
def intro_tweet() -> Tweet:
    """
    Twitter API の公式リファレンスのサンプルに記載されていたツイート。
    """

    return Tweet(
        id="1460323737035677698",
        text=dedent(
            """
            Introducing a new era for the Twitter Developer Platform! \n
            📣The Twitter API v2 is now the primary API and full of new features
            ⏱Immediate access for most use cases, or apply to get more access for free
            📖Removed certain restrictions in the Policy
            https://t.co/Hrm15bkBWJ https://t.co/YFfCDErHsg
            """
        ).strip(),
        edit_history_tweet_ids=["1460323737035677698"],
    )


@pytest.fixture
def twitter_dev_user() -> User:
    return User(
        id="2244994945",
        name="Twitter Dev",
        username="TwitterDev",
    )
