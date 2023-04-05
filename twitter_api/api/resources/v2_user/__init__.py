from typing import Literal

from .get_v2_user import V2GetUserResources

V2UserUrl = Literal["https://api.twitter.com/2/users/:id"]


class V2UserResources(V2GetUserResources):
    pass
