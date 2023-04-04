from typing import TypedDict

from twitter_api.api.v2.types.media.media_id import MediaId

DmConversationAttachment = TypedDict(
    "DmConversationAttachment",
    {
        "media_id": MediaId,
    },
)
