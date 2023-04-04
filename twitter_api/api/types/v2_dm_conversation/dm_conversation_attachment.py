from typing import TypedDict

from twitter_api.api.types.v2_media.media_id import MediaId

DmConversationAttachment = TypedDict(
    "DmConversationAttachment",
    {
        "media_id": MediaId,
    },
)
