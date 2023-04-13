import pytest

from tests.conftest import synthetic_monitoring_is_disable
from twitter_api.client.twitter_api_client import TwitterApiClient
from twitter_api.client.twitter_api_real_client import TwitterApiRealClient


class TestTwitterApiClient:
    def test_client_constructor(self):
        """
        TwitterApiClient でのコンストラクタによる生成を禁止する。

        TwitterApiClient.from_* 系統の表現によるインスタンス化しか許可しない。
        """
        with pytest.raises(TypeError):
            TwitterApiClient()  # type: ignore

    @pytest.mark.skipif(**synthetic_monitoring_is_disable())
    def test_client_from_oauth2_bearer_token(self):
        assert isinstance(
            TwitterApiClient.from_oauth2_bearer_token_env(),
            TwitterApiRealClient,
        )

    @pytest.mark.skipif(**synthetic_monitoring_is_disable())
    def test_client_from_oauth2_app_env(self):
        assert isinstance(
            TwitterApiClient.from_oauth2_app_env(),
            TwitterApiRealClient,
        )

    @pytest.mark.skipif(**synthetic_monitoring_is_disable())
    def test_client_from_oauth1_app_env(self):
        assert isinstance(
            TwitterApiClient.from_oauth1_app_env(),
            TwitterApiRealClient,
        )
