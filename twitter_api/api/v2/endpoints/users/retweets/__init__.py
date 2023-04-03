from typing import Literal

from .post_user_retweets import V2PostUserFollowingResources

UserFollowingUrl = Literal["https://api.twitter.com/2/users/:id/following"]


class V2UserFollowingResources(V2PostUserFollowingResources):
    pass
