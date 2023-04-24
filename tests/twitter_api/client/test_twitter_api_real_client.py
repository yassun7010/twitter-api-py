import pytest

from tests.conftest import synthetic_monitoring_is_disable
from twitter_api.client.twitter_api_real_client import TwitterApiRealClient


class TestTwitterApiRealClient:
    @pytest.mark.skipif(**synthetic_monitoring_is_disable())
    def test_real_client_from_oauth2_bearer_token(self):
        assert isinstance(
            TwitterApiRealClient.from_oauth2_bearer_token_env(),
            TwitterApiRealClient,
        )

    @pytest.mark.skipif(**synthetic_monitoring_is_disable())
    def test_real_client_from_oauth2_app_env(self):
        assert isinstance(
            TwitterApiRealClient.from_oauth2_app_env(),
            TwitterApiRealClient,
        )

    @pytest.mark.skipif(**synthetic_monitoring_is_disable())
    def test_real_client_from_oauth1_app_env(self):
        assert isinstance(
            TwitterApiRealClient.from_oauth1_app_env(),
            TwitterApiRealClient,
        )

    @pytest.mark.skipif(**synthetic_monitoring_is_disable())
    def test_client_close(self):
        TwitterApiRealClient.from_oauth2_app_env().close()

    @pytest.mark.skipif(**synthetic_monitoring_is_disable())
    def test_client_with(self):
        with TwitterApiRealClient.from_oauth2_app_env() as client:
            assert isinstance(client, TwitterApiRealClient)
