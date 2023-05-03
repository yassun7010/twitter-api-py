from typing import Union

from twitter_api.types.v2_user.user_id import UserId
from twitter_api.types.v2_user.username import Username

from ._specific_keyword import SpecificKeyword
from .operator import Operator


class FromUser(SpecificKeyword, Operator):
    def __init__(self, user: Union[UserId, Username]):
        super().__init__(user, "from:")
