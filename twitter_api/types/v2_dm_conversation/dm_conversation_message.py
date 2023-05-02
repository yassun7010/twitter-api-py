from typing import NotRequired, Optional, TypedDict, Union

from twitter_api.types.v2_dm_conversation.dm_conversation_attachment import (
    DmConversationAttachment,
)

DmConversationAttachmentOnly = TypedDict(
    "DmConversationMessage",
    {
        "attachments": list[DmConversationAttachment],
    },
)

DmConversationMessageText = TypedDict(
    "DmConversationMessage",
    {
        "text": str,
        "attachments": NotRequired[Optional[list[DmConversationAttachment]]],
    },
)

DmConversationMessage = Union[
    DmConversationAttachmentOnly,
    DmConversationMessageText,
]
