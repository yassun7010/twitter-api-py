import pytest

from tests.conftest import synthetic_monitoring_is_disable
from twitter_api.client.twitter_api_async_real_client import TwitterApiAsyncRealClient


class TestTwitterApiAsyncRealClient:
    @pytest.mark.skipif(**synthetic_monitoring_is_disable())
    def test_real_client(self, oauth2_app_async_real_client: TwitterApiAsyncRealClient):
        # インターフェースの未実装がないかをテストする。
        # TestTwitterApiMockClient はテストで必ずテストされるので、テスト不要。
        assert isinstance(oauth2_app_async_real_client, TwitterApiAsyncRealClient)

    @pytest.mark.skipif(**synthetic_monitoring_is_disable())
    def test_real_client_from_oauth2_bearer_token(self):
        assert isinstance(
            TwitterApiAsyncRealClient.from_oauth2_bearer_token_env(),
            TwitterApiAsyncRealClient,
        )

    @pytest.mark.skipif(**synthetic_monitoring_is_disable())
    def test_real_client_from_oauth2_app_env(self):
        assert isinstance(
            TwitterApiAsyncRealClient.from_oauth2_app_env(),
            TwitterApiAsyncRealClient,
        )

    @pytest.mark.skipif(**synthetic_monitoring_is_disable())
    def test_real_client_from_oauth1_app_env(self):
        assert isinstance(
            TwitterApiAsyncRealClient.from_oauth1_app_env(),
            TwitterApiAsyncRealClient,
        )
