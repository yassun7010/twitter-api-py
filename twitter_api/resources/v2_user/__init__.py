from typing import Literal

from .get_v2_user import AsyncGetV2UserResources, GetV2UserResources

V2UserUrl = Literal["https://api.twitter.com/2/users/:id"]


class V2UserResources(GetV2UserResources):
    pass


class AsyncV2UserResources(AsyncGetV2UserResources):
    pass
