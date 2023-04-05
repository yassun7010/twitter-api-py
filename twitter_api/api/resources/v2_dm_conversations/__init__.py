from typing import TypeAlias

from typing_extensions import Literal

from .post_v2_dm_conversations import PostV2DmConversationsResources

V2DmConversationsUrl: TypeAlias = Literal["https://api.twitter.com/2/dm_conversations"]


class V2DmConversationsResources(PostV2DmConversationsResources):
    pass
