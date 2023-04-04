from typing import TypeAlias

from typing_extensions import Literal

from .post_dm_conversations import V2PostDmConversationsResources

DmConversationsUrl: TypeAlias = Literal["https://api.twitter.com/2/dm_conversations"]


class V2DmConversationsResources(V2PostDmConversationsResources):
    pass
