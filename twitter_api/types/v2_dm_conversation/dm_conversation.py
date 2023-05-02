from twitter_api.types.extra_permissive_model import ExtraPermissiveModel
from twitter_api.types.v2_dm_conversation.dm_conversation_id import DmConversationId
from twitter_api.types.v2_dm_event.dm_event_id import DmEventId


class DmConversation(ExtraPermissiveModel):
    dm_conversation_id: DmConversationId
    dm_event_id: DmEventId
