from typing import TypeAlias

from typing_extensions import Literal

from .post_v2_dm_conversations_with_participant_messages import (
    AsyncPostV2DmConversationsWithParticipantMessagesResources,
    PostV2DmConversationsWithParticipantMessagesResources,
)

V2DmConversationsWithParticipantMessagesUrl: TypeAlias = Literal[
    "https://api.twitter.com/2/dm_conversations/with/:participant_id/messages"
]


class V2DmConversationsWithParticipantMessagesResources(
    PostV2DmConversationsWithParticipantMessagesResources
):
    pass


class AsyncV2DmConversationsWithParticipantMessagesResources(
    AsyncPostV2DmConversationsWithParticipantMessagesResources
):
    pass
