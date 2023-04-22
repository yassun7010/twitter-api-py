import pytest

from tests.conftest import synthetic_monitoring_is_disable
from twitter_api.client.twitter_api_async_client import TwitterApiAsyncClient
from twitter_api.client.twitter_api_async_real_client import TwitterApiAsyncRealClient
from twitter_api.client.twitter_api_real_client import TwitterApiRealClient


class TestTwitterApiAsyncClient:
    def test_client_constructor(self):
        """
        TwitterApiAsyncClient でのコンストラクタによる生成を禁止する。

        TwitterApiAsyncClient.from_* 系統の表現によるインスタンス化しか許可しない。
        """
        with pytest.raises(TypeError):
            TwitterApiAsyncClient()  # type: ignore

    @pytest.mark.skipif(**synthetic_monitoring_is_disable())
    def test_client_from_oauth2_bearer_token(self):
        assert isinstance(
            TwitterApiAsyncClient.from_oauth2_bearer_token_env(),
            TwitterApiAsyncRealClient,
        )

    @pytest.mark.skipif(**synthetic_monitoring_is_disable())
    def test_client_from_oauth2_app_env(self):
        assert isinstance(
            TwitterApiAsyncClient.from_oauth2_app_env(),
            TwitterApiAsyncRealClient,
        )

    @pytest.mark.skipif(**synthetic_monitoring_is_disable())
    def test_client_from_oauth1_app_env(self):
        assert isinstance(
            TwitterApiAsyncClient.from_oauth1_app_env(),
            TwitterApiAsyncRealClient,
        )

    @pytest.mark.asyncio
    @pytest.mark.skipif(**synthetic_monitoring_is_disable())
    async def test_client_async_with(self):
        async with TwitterApiAsyncClient.from_oauth2_app_env() as client:
            assert isinstance(client, TwitterApiAsyncClient)
