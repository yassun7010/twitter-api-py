from typing import Literal

from .post_v2_user_following import (
    AsyncPostV2UserFollowingResources,
    PostV2UserFollowingResources,
)

V2UserFollowingUrl = Literal["https://api.twitter.com/2/users/:id/following"]


class V2UserFollowingResources(PostV2UserFollowingResources):
    pass


class AsyncV2UserFollowingResources(AsyncPostV2UserFollowingResources):
    pass
