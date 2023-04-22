from typing import TypeAlias

from typing_extensions import Literal

from .post_v2_dm_conversations_messages import (
    AsyncPostV2DmConversationMessagesResources,
    PostV2DmConversationMessagesResources,
)

V2DmConversationsMessagesUrl: TypeAlias = Literal[
    "https://api.twitter.com/2/dm_conversations/:dm_conversation_id/messages"
]


class V2DmConversationMessagesResources(PostV2DmConversationMessagesResources):
    pass


class AsyncV2DmConversationMessagesResources(
    AsyncPostV2DmConversationMessagesResources
):
    pass
