from typing import TypeAlias

from typing_extensions import Literal

from .get_v2_dm_conversations_with_participant_dm_events import (
    AsyncGetV2DmConversationsWithParticipantDmEventsResources,
    GetV2DmConversationsWithParticipantDmEventsResources,
)

V2DmConversationsWithParticipantDmEventsUrl: TypeAlias = Literal[
    "https://api.twitter.com/2/dm_conversations/with/:participant_id/dm_events"
]


class V2DmConversationsWithParticipantDmEventsResources(
    GetV2DmConversationsWithParticipantDmEventsResources
):
    pass


class AsyncV2DmConversationsWithParticipantDmEventsResources(
    AsyncGetV2DmConversationsWithParticipantDmEventsResources
):
    pass
