from twitter_api.types.v2_list.list_id import ListId

from .operator import InvertableOperator, Operator, StandaloneOperator


class ListOperator(
    InvertableOperator[Operator],
    StandaloneOperator[Operator],
):
    def __init__(self, id: ListId):
        self._value = id

    def __str__(self) -> str:
        return f"list:{self._value}"
