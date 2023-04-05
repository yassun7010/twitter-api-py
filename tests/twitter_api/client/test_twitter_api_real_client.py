import pytest

from tests.conftest import synthetic_monitoring_is_disable
from twitter_api.client.twitter_api_real_client import TwitterApiRealClient


class TestTwitterApiRealClient:
    @pytest.mark.skipif(**synthetic_monitoring_is_disable())
    def test_real_client(self, real_app_auth_v2_client: TwitterApiRealClient):
        # インターフェースの未実装がないかをテストする。
        # TestTwitterApiMockClient はテストで必ずテストされるので、テスト不要。
        assert isinstance(real_app_auth_v2_client, TwitterApiRealClient)

    @pytest.mark.skipif(**synthetic_monitoring_is_disable())
    def test_real_client_from_app_oauth2_bearer_token(self):
        assert isinstance(
            TwitterApiRealClient.from_app_oauth2_bearer_token_env(),
            TwitterApiRealClient,
        )

    @pytest.mark.skipif(**synthetic_monitoring_is_disable())
    def test_real_client_from_app_oauth2_env(self):
        assert isinstance(
            TwitterApiRealClient.from_app_oauth2_env(),
            TwitterApiRealClient,
        )

    @pytest.mark.skipif(**synthetic_monitoring_is_disable())
    def test_real_client_from_user_oauth1_env(self):
        assert isinstance(
            TwitterApiRealClient.from_user_oauth1_env(),
            TwitterApiRealClient,
        )
