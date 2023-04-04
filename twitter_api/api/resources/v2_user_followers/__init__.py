from typing import Literal

from .get_user_followers import V2GetUserFollowersResources

V2UserFollowersUrl = Literal["https://api.twitter.com/2/users/:id/followers"]


class V2UserFollowersResources(V2GetUserFollowersResources):
    pass
