from typing import Literal

from .get_v2_users import AsyncGetV2UsersResources, GetV2UsersResources

V2UsersUrl = Literal["https://api.twitter.com/2/users"]


class V2UsersResources(GetV2UsersResources):
    pass


class AsyncV2UsersResources(AsyncGetV2UsersResources):
    pass
