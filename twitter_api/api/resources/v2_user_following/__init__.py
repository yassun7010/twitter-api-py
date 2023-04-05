from typing import Literal

from .post_v2_user_following import PostV2UserFollowingResources

V2UserFollowingUrl = Literal["https://api.twitter.com/2/users/:id/following"]


class V2UserFollowingResources(PostV2UserFollowingResources):
    pass
