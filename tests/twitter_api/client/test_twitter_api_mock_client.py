from twitter_api.client.twitter_api_mock_client import TwitterApiMockClient


class TestTwitterApiMockClient:
    def test_mock_client_from_app_oauth2_bearer_token(self):
        assert isinstance(
            TwitterApiMockClient.from_app_oauth2_bearer_token_env(),
            TwitterApiMockClient,
        )

    def test_mock_client_from_app_oauth2_env(self):
        assert isinstance(
            TwitterApiMockClient.from_app_oauth2_env(),
            TwitterApiMockClient,
        )

    def test_mock_client_from_user_oauth1_env(self):
        assert isinstance(
            TwitterApiMockClient.from_user_oauth1_env(),
            TwitterApiMockClient,
        )
