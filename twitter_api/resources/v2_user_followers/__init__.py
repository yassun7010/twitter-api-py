from typing import Literal

from .get_v2_user_followers import (
    AsyncGetV2UserFollowersResources,
    GetV2UserFollowersResources,
)

V2UserFollowersUrl = Literal["https://api.twitter.com/2/users/:id/followers"]


class V2UserFollowersResources(GetV2UserFollowersResources):
    pass


class AsyncV2UserFollowersResources(AsyncGetV2UserFollowersResources):
    pass
