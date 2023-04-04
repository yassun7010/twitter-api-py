from typing import Literal

from .post_user_following import V2PostUserFollowingResources

V2UserFollowingUrl = Literal["https://api.twitter.com/2/users/:id/following"]


class V2UserFollowingResources(V2PostUserFollowingResources):
    pass
