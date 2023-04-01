import pytest

from tests.conftest import synthetic_monitoring_is_disable
from twitter_api.client.twitter_api_client import TwitterApiClient
from twitter_api.client.twitter_api_real_client import TwitterApiRealClient


class TestTwitterApiClient:
    def test_client(self, client):
        # インターフェースの未実装がないかをテストする。
        # TestTwitterApiMockClient はテストで必ずテストされるので、テスト不要。
        assert True

    def test_client_constructor(self):
        """
        TwitterApiClient でのコンストラクタによる生成を禁止する。

        TwitterApiClient.from_* 系統の表現によるインスタンス化しか許可しない。
        """
        with pytest.raises(TypeError):
            TwitterApiClient()  # type: ignore

    @pytest.mark.skipif(**synthetic_monitoring_is_disable())
    def test_client_from_bearer_token(self):
        assert isinstance(
            TwitterApiClient.from_bearer_token_env(),
            TwitterApiRealClient,
        )

    @pytest.mark.skipif(**synthetic_monitoring_is_disable())
    def test_client_from_app_auth_v2_env(self):
        assert isinstance(
            TwitterApiClient.from_app_auth_v2_env(),
            TwitterApiRealClient,
        )

    @pytest.mark.skipif(**synthetic_monitoring_is_disable())
    def test_client_from_user_auth_v1_env(self):
        assert isinstance(
            TwitterApiClient.from_user_auth_v1_env(),
            TwitterApiRealClient,
        )
