from typing import Literal

DmEventField = Literal[
    "id",
    "text",
    "event_type",
    "created_at",
    "dm_conversation_id",
    "sender_id",
    "participant_ids",
    "referenced_tweets",
    "attachments",
]

ALL_DM_EVENT_FIELDS: list[DmEventField] = [
    "id",
    "text",
    "event_type",
    "created_at",
    "dm_conversation_id",
    "sender_id",
    "participant_ids",
    "referenced_tweets",
    "attachments",
]
