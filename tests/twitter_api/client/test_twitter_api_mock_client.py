from twitter_api.client.twitter_api_mock_client import TwitterApiMockClient


class TestTwitterApiMockClient:
    def test_mock_client_from_oauth2_bearer_token(self):
        assert isinstance(
            TwitterApiMockClient.from_oauth2_bearer_token_env(),
            TwitterApiMockClient,
        )

    def test_mock_client_from_oauth2_app_env(self):
        assert isinstance(
            TwitterApiMockClient.from_oauth2_app_env(),
            TwitterApiMockClient,
        )

    def test_mock_client_from_oauth1_user_env(self):
        assert isinstance(
            TwitterApiMockClient.from_oauth1_user_env(),
            TwitterApiMockClient,
        )
