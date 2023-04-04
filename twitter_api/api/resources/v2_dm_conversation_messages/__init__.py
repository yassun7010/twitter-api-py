from typing import TypeAlias

from typing_extensions import Literal

from .post_dm_conversations_messages import (
    V2PostDmConversationMessagesResources,
    V2PostDmConversationMessagesResponseBody,
)

DmConversationsMessagesUrl: TypeAlias = Literal[
    "https://api.twitter.com/2/dm_conversations/:dm_conversation_id/messages"
]


class V2DmConversationMessagesResources(V2PostDmConversationMessagesResources):
    pass


__all__ = [
    "V2PostDmConversationMessagesResponseBody",
    "V2DmConversationMessagesResources",
    "V2PostDmConversationMessagesResources",
]
