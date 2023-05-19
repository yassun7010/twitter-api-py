import pytest

from twitter_api.client.twitter_api_async_mock_client import TwitterApiAsyncMockClient
from twitter_api.error import MockResponseBodyRemainsError
from twitter_api.resources.v2_tweet.get_v2_tweet import GetV2TweetResponseBody
from twitter_api.types.v2_scope import ALL_SCOPES
from twitter_api.types.v2_tweet.tweet import Tweet


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

    @pytest.mark.asyncio
    async def test_mock_client_request(self, intro_tweet: Tweet):
        async with TwitterApiAsyncMockClient.from_oauth2_app_env() as client:
            response_body = GetV2TweetResponseBody(data=intro_tweet)

            assert (
                await (
                    client.chain()
                    .inject_get_response_body(
                        "https://api.twitter.com/2/tweets/:id",
                        response_body,
                    )
                    .request("https://api.twitter.com/2/tweets/:id")
                    .get(intro_tweet.id)
                )
                == response_body
            )

    @pytest.mark.asyncio
    async def test_mock_client_raise_response_body_remain_error(
        self, intro_tweet: Tweet
    ):
        with pytest.raises(MockResponseBodyRemainsError):
            async with TwitterApiAsyncMockClient.from_oauth2_app_env() as client:
                response_body = GetV2TweetResponseBody(data=intro_tweet)

                assert (
                    await (
                        client.chain()
                        .inject_get_response_body(
                            "https://api.twitter.com/2/tweets/:id",
                            response_body,
                        )
                        .inject_get_response_body(
                            "https://api.twitter.com/2/tweets/:id",
                            response_body,
                        )
                        .request("https://api.twitter.com/2/tweets/:id")
                        .get(intro_tweet.id)
                    )
                    == response_body
                )
