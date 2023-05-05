from twitter_api.types.v2_dm_conversation.dm_conversation_id import DmConversationId

from .operator import InvertibleOperator, StandaloneOperator


class ConversationIdOperator(
    InvertibleOperator,
    StandaloneOperator,
):
    def __init__(self, id: DmConversationId):
        self._value = id

    def __str__(self) -> str:
        return f"conversation_id:{self._value}"
