from typing import Literal

from .get_v2_users_by import AsyncGetV2UsersByResources, GetV2UsersByResources

V2UsersByUrl = Literal["https://api.twitter.com/2/users/by"]


class V2UsersByResources(GetV2UsersByResources):
    pass


class AsyncV2UsersByResources(AsyncGetV2UsersByResources):
    pass
