from typing import Literal

from twitter_api.client.request.request_client import RequestClient

from .get_user_followers import V2GetUserFollowers

UserFollowersUrl = Literal["https://api.twitter.com/2/users/:id/followers"]


class V2UserFollowers(V2GetUserFollowers):
    def __init__(self, client: RequestClient) -> None:
        self._client = client

    @property
    def request_client(self) -> RequestClient:
        return self._client
