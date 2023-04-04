from typing import Literal

from .get_users import V2GetUsersResources

UsersUrl = Literal["https://api.twitter.com/2/users"]


class V2UsersResources(V2GetUsersResources):
    pass
