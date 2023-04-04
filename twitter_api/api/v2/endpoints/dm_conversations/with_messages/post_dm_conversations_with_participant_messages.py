from typing import NotRequired, Optional, TypedDict, Union

from twitter_api.api.api_resources import ApiResources
from twitter_api.api.v2.types.dm_conversation.dm_conversation_id import DmConversationId
from twitter_api.api.v2.types.dm_event.dm_event_id import DmEventId
from twitter_api.api.v2.types.media.media_id import MediaId
from twitter_api.api.v2.types.user.user_id import UserId
from twitter_api.rate_limit.rate_limit_decorator import rate_limit
from twitter_api.types.endpoint import Endpoint
from twitter_api.types.extra_permissive_model import ExtraPermissiveModel
from twitter_api.types.http import downcast_dict

ENDPOINT = Endpoint(
    "POST", "https://api.twitter.com/2/dm_conversations/with/:participant_id/messages"
)

V2PostDmConversationsWithParticipantMessagesRequestBodyAttachment = TypedDict(
    "V2PostDmConversationsWithParticipantMessagesRequestBodyAttachment",
    {
        "media_id": MediaId,
    },
)

V2PostDmConversationsWithParticipantMessagesRequestBodyAttachmentOnly = TypedDict(
    "V2PostDmConversationsWithParticipantMessagesRequestBody",
    {
        "attachments": V2PostDmConversationsWithParticipantMessagesRequestBodyAttachment,
    },
)

V2PostDmConversationsWithParticipantMessagesRequestBodyText = TypedDict(
    "V2PostDmConversationsWithParticipantMessagesRequestBody",
    {
        "text": str,
        "attachments": NotRequired[
            Optional[V2PostDmConversationsWithParticipantMessagesRequestBodyAttachment]
        ],
    },
)

V2PostDmConversationsWithParticipantMessagesRequestBody = Union[
    V2PostDmConversationsWithParticipantMessagesRequestBodyText,
    V2PostDmConversationsWithParticipantMessagesRequestBodyAttachmentOnly,
]


class V2PostDmConversationsWithParticipantMessagesResponseBody(ExtraPermissiveModel):
    dm_conversation_id: DmConversationId
    dm_event_id: DmEventId


class V2PostDmConversationsWithParticipantMessagesResources(ApiResources):
    @rate_limit(ENDPOINT, "user", requests=200, mins=15)
    @rate_limit(ENDPOINT, "user", requests=1000, hours=24)
    @rate_limit(ENDPOINT, "app", requests=15000, hours=24)
    def post(
        self,
        participant_id: UserId,
        request_body: V2PostDmConversationsWithParticipantMessagesRequestBody,
    ) -> V2PostDmConversationsWithParticipantMessagesResponseBody:
        # flake8: noqa E501
        """
        Direct Message を送る。

        refer: https://developer.twitter.com/en/docs/twitter-api/direct-messages/manage/api-reference/post-dm_conversations-with-participant_id-messages
        """
        return self.request_client.post(
            endpoint=ENDPOINT,
            url=ENDPOINT.url.replace(":participant_id", participant_id),
            json=downcast_dict(request_body),
            response_type=V2PostDmConversationsWithParticipantMessagesResponseBody,
        )
