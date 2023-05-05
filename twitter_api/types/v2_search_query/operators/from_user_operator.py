from typing import Union

from twitter_api.types.v2_user.user_id import UserId
from twitter_api.types.v2_user.username import Username

from .operator import InvertibleOperator, StandaloneOperator


class FromUserOperator(
    InvertibleOperator,
    StandaloneOperator,
):
    def __init__(self, user: Union[UserId, Username]):
        self._value = user

    def __str__(self) -> str:
        return f"from:{self._value}"
