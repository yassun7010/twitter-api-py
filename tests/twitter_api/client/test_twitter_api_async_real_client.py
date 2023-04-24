import pytest

from tests.conftest import synthetic_monitoring_is_disable
from twitter_api.client.twitter_api_async_real_client import TwitterApiAsyncRealClient


class TestTwitterApiAsyncRealClient:
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

    @pytest.mark.asyncio
    @pytest.mark.skipif(**synthetic_monitoring_is_disable())
    async def test_client_aclose(self):
        await TwitterApiAsyncRealClient.from_oauth2_app_env().aclose()

    @pytest.mark.asyncio
    @pytest.mark.skipif(**synthetic_monitoring_is_disable())
    async def test_real_client_from_oauth2_bearer_token_with_async(self):
        async with TwitterApiAsyncRealClient.from_oauth2_bearer_token_env() as client:
            assert isinstance(client, TwitterApiAsyncRealClient)

    @pytest.mark.asyncio
    @pytest.mark.skipif(**synthetic_monitoring_is_disable())
    async def test_real_client_from_oauth2_app_env_with_async(self):
        async with TwitterApiAsyncRealClient.from_oauth2_app_env() as client:
            assert isinstance(client, TwitterApiAsyncRealClient)

    @pytest.mark.asyncio
    @pytest.mark.skipif(**synthetic_monitoring_is_disable())
    async def test_real_client_from_oauth1_app_env_with_async(self):
        async with TwitterApiAsyncRealClient.from_oauth1_app_env() as client:
            assert isinstance(client, TwitterApiAsyncRealClient)
