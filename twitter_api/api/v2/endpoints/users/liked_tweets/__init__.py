from typing import Literal

from twitter_api.client.request.request_client import RequestClient

from .get_user_liked_tweets import V2GetUserLikedTweets

UserLikedTweetsUrl = Literal["https://api.twitter.com/2/users/:id/liked_tweets"]


class V2UserLikedTweets(V2GetUserLikedTweets):
    def __init__(self, client: RequestClient) -> None:
        self._client = client

    @property
    def request_client(self) -> RequestClient:
        return self._client
