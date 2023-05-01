import pytest

from twitter_api.api.types.v2_scope import ALL_SCOPES
from twitter_api.client.twitter_api_async_mock_client import TwitterApiAsyncMockClient


class TestTwitterApiAsyncMockClient:
    def test_mock_client_from_oauth2_bearer_token(self):
        assert isinstance(
            TwitterApiAsyncMockClient.from_oauth2_bearer_token_env(),
            TwitterApiAsyncMockClient,
        )

    def test_mock_client_from_oauth2_app_env(self):
        assert isinstance(
            TwitterApiAsyncMockClient.from_oauth2_app_env(),
            TwitterApiAsyncMockClient,
        )

    def test_mock_client_from_oauth2_user_env(self):
        assert isinstance(
            (
                TwitterApiAsyncMockClient.from_oauth2_user_flow_env(scope=ALL_SCOPES)
                .request("https://twitter.com/i/oauth2/authorize")
                .generate_authorization_url()
                .input_response_url("https://localhost:3000")
                .request("https://api.twitter.com/2/oauth2/token")
                .post()
                .generate_client()
            ),
            TwitterApiAsyncMockClient,
        )

    def test_mock_client_from_oauth1_app_env(self):
        assert isinstance(
            TwitterApiAsyncMockClient.from_oauth1_app_env(),
            TwitterApiAsyncMockClient,
        )

    def test_mock_client_from_oauth1_user_env(self):
        assert isinstance(
            (
                TwitterApiAsyncMockClient.from_oauth1_user_flow_env()
                .request("https://api.twitter.com/oauth/request_token")
                .post()
                .request("https://api.twitter.com/oauth/authorize")
                .generate_authorization_url()
                .input_response_url("https://localhost:3000")
                .request("https://api.twitter.com/oauth/access_token")
                .post()
                .generate_client()
            ),
            TwitterApiAsyncMockClient,
        )

    @pytest.mark.asyncio
    async def test_client_aclose(self):
        await TwitterApiAsyncMockClient.from_oauth2_app_env().aclose()

    @pytest.mark.asyncio
    async def test_mock_client_from_oauth2_bearer_token_async_with(self):
        async with TwitterApiAsyncMockClient.from_oauth2_bearer_token_env() as client:
            assert isinstance(client, TwitterApiAsyncMockClient)

    @pytest.mark.asyncio
    async def test_mock_client_from_oauth2_app_env_async_with(self):
        async with TwitterApiAsyncMockClient.from_oauth2_app_env() as client:
            assert isinstance(client, TwitterApiAsyncMockClient)

    @pytest.mark.asyncio
    async def test_mock_client_from_oauth2_user_env_async_with(self):
        async with (
            TwitterApiAsyncMockClient.from_oauth2_user_flow_env(scope=ALL_SCOPES)
            .request("https://twitter.com/i/oauth2/authorize")
            .generate_authorization_url()
            .input_response_url("https://localhost:3000")
            .request("https://api.twitter.com/2/oauth2/token")
            .post()
            .generate_client()
        ) as client:
            assert isinstance(client, TwitterApiAsyncMockClient)

    @pytest.mark.asyncio
    async def test_mock_client_from_oauth1_app_env_async_with(self):
        async with TwitterApiAsyncMockClient.from_oauth1_app_env() as client:
            assert isinstance(client, TwitterApiAsyncMockClient)

    @pytest.mark.asyncio
    async def test_mock_client_from_oauth1_user_env_async_with(self):
        async with (
            TwitterApiAsyncMockClient.from_oauth1_user_flow_env()
            .request("https://api.twitter.com/oauth/request_token")
            .post()
            .request("https://api.twitter.com/oauth/authorize")
            .generate_authorization_url()
            .input_response_url("https://localhost:3000")
            .request("https://api.twitter.com/oauth/access_token")
            .post()
            .generate_client()
        ) as client:
            assert isinstance(
                client,
                TwitterApiAsyncMockClient,
            )
