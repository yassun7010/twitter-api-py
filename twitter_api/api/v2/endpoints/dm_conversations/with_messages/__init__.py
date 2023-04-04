from typing import TypeAlias

from typing_extensions import Literal

from .post_dm_conversations_with_participant_messages import (
    V2PostDmConversationsWithParticipantMessagesResources,
)

DmConversationsWithParticipantMessagesUrl: TypeAlias = Literal[
    "https://api.twitter.com/2/dm_conversations/with/:participant_id/messages"
]


class V2DmConversationsWithParticipantMessagesResources(
    V2PostDmConversationsWithParticipantMessagesResources
):
    pass
