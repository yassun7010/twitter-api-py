from typing import Literal, TypeAlias

DmEventExpansion: TypeAlias = Literal[
    "attachments.media_keys",
    "participant_ids",
    "referenced_tweets.id",
    "sender_id",
]

ALL_DM_EVENT_EXPANSIONS: list[DmEventExpansion] = [
    "attachments.media_keys",
    "participant_ids",
    "referenced_tweets.id",
    "sender_id",
]
