from typing import Literal, NotRequired, Optional, TypedDict, Union

from twitter_api.api.resources.api_resources import ApiResources
from twitter_api.api.types.v2_dm_conversation.dm_conversation_attachment import (
    DmConversationAttachment,
)
from twitter_api.api.types.v2_dm_conversation.dm_conversation_id import DmConversationId
from twitter_api.api.types.v2_dm_conversation.dm_conversation_message import (
    DmConversationMessage,
)
from twitter_api.api.types.v2_dm_event.dm_event_id import DmEventId
from twitter_api.api.types.v2_media.media_id import MediaId
from twitter_api.api.types.v2_user.user_id import UserId
from twitter_api.rate_limit.rate_limit_decorator import rate_limit
from twitter_api.types.endpoint import Endpoint
from twitter_api.types.extra_permissive_model import ExtraPermissiveModel
from twitter_api.types.http import downcast_dict

ENDPOINT = Endpoint("POST", "https://api.twitter.com/2/dm_conversations")


V2PostDmConversationsRequestBody = TypedDict(
    "V2PostDmConversationsRequestBody",
    {
        "conversation_type": Literal["Group"],
        "message": DmConversationMessage,
        "participant_ids": list[UserId],
    },
)


class V2PostDmConversationsResponseBody(ExtraPermissiveModel):
    dm_conversation_id: DmConversationId
    dm_event_id: DmEventId


class V2PostDmConversationsResources(ApiResources):
    @rate_limit(ENDPOINT, "user", requests=200, mins=15)
    @rate_limit(ENDPOINT, "user", requests=1000, hours=24)
    @rate_limit(ENDPOINT, "app", requests=15000, hours=24)
    def post(
        self,
        participant_id: UserId,
        request_body: V2PostDmConversationsRequestBody,
    ) -> V2PostDmConversationsResponseBody:
        # flake8: noqa E501
        """
        DM 用の新しい会話グループを作成する。

        refer: https://developer.twitter.com/en/docs/twitter-api/direct-messages/manage/api-reference/post-dm_conversations
        """
        return self.request_client.post(
            endpoint=ENDPOINT,
            json=downcast_dict(request_body),
            response_type=V2PostDmConversationsResponseBody,
        )
