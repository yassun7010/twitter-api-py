from twitter_api.api.v2.endpoints.tweets.get_tweet import GetTweetResponseBody
from twitter_api.client.twitter_api_mock_client import TwitterApiMockClient
from twitter_api.client.twitter_api_real_client import TwitterApiRealClient


class TestOauth2PostInvalidateToken:
    def test_get_tweets(self, real_client: TwitterApiRealClient, tweet):
        expected_response = GetTweetResponseBody(data=tweet)
        real_response = real_client.request("/2/tweets/:id").get(tweet.id)

        print(real_response.dict())
        print(expected_response.dict())

        assert real_response == expected_response


class TestMockOauth2PostInvalidateToken:
    def test_mock_get_tweets(self, mock_client: TwitterApiMockClient, tweet):
        expected_response = GetTweetResponseBody(data=tweet)

        assert (
            mock_client.chain()
            .inject_get_response("/2/tweets/:id", expected_response)
            .request("/2/tweets/:id")
            .get(tweet.id)
            == expected_response
        )
