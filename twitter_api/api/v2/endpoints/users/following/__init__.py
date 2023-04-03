from typing import Literal

from twitter_api.client.request.request_client import RequestClient

from .post_user_following import V2PostUserFollowingResources

UserFollowingUrl = Literal["https://api.twitter.com/2/users/:id/following"]


class V2UserFollowingResources(V2PostUserFollowingResources):
    def __init__(self, client: RequestClient) -> None:
        self._client = client

    @property
    def request_client(self) -> RequestClient:
        return self._client
