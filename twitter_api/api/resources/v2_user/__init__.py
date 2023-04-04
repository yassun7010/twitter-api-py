from typing import Literal

from .get_user import V2GetUserResources

UserUrl = Literal["https://api.twitter.com/2/users/:id"]


class V2UserResources(V2GetUserResources):
    pass
