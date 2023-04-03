from typing import Literal

from twitter_api.api.v2.endpoints.users.get_user import V2GetUserResources

from .get_users import V2GetUsersResources

UsersUrl = Literal["https://api.twitter.com/2/users"]
UserUrl = Literal["https://api.twitter.com/2/users/:id"]


class V2UserResources(V2GetUserResources):
    pass


class V2UsersResources(V2GetUsersResources):
    pass
