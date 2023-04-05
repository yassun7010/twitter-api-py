from typing import TypeAlias

from typing_extensions import Literal

from .post_v2_dm_conversations import V2PostDmConversationsResources

V2DmConversationsUrl: TypeAlias = Literal["https://api.twitter.com/2/dm_conversations"]


class V2DmConversationsResources(V2PostDmConversationsResources):
    pass
