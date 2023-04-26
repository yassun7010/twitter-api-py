from typing import Literal

from .get_v2_users_by_username import (
    AsyncGetV2UsersByUsernameResources,
    GetV2UsersByUsernameResources,
)

V2UsersByUsernameUrl = Literal["https://api.twitter.com/2/users/by/username/:username"]


class V2UsersByUsernameResources(GetV2UsersByUsernameResources):
    pass


class AsyncV2UsersByUsernameResources(AsyncGetV2UsersByUsernameResources):
    pass
