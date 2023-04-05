from typing import Literal

from .get_v2_users import V2GetUsersResources

V2UsersUrl = Literal["https://api.twitter.com/2/users"]


class V2UsersResources(V2GetUsersResources):
    pass
