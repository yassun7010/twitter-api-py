from typing_extensions import Literal

from twitter_api.client.request.request_client import RequestClient

from .delete_tweet import V2DeleteTweet
from .get_tweet import V2GetTweet
from .get_tweets import V2GetTweets
from .post_tweet import V2PostTweet

TweetsUrl = Literal["https://api.twitter.com/2/tweets"]
TweetUrl = Literal["https://api.twitter.com/2/tweets/:id"]


class V2Tweets(V2GetTweets, V2PostTweet):
    def __init__(self, client: RequestClient) -> None:
        self._client = client

    @property
    def request_client(self) -> RequestClient:
        return self._client


class V2Tweet(V2GetTweet, V2DeleteTweet):
    def __init__(self, client: RequestClient) -> None:
        self._client = client

    @property
    def request_client(self) -> RequestClient:
        return self._client
