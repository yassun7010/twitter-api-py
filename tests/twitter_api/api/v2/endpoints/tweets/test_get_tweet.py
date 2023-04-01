from twitter_api.api.v2.endpoints.tweets.get_tweet import GetTweetResponseBody
from twitter_api.api.v2.types.tweet.tweet import Tweet
from twitter_api.client.twitter_api_mock_client import TwitterApiMockClient


class TestTwitterApiMockClient:
    def test_mock_get_tweets(self, mock_client: TwitterApiMockClient):
        tweet = Tweet(
            id="12345",
            text="tweet",
            edit_history_tweet_ids=["56789"],
        )
        response = GetTweetResponseBody(data=tweet)

        assert (
            mock_client.chain()
            .inject_get_response("/2/tweets/:id", response)
            .request("/2/tweets/:id")
            .get(tweet.id)
            == response
        )
