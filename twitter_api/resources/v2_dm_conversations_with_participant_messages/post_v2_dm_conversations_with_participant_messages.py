from twitter_api.rate_limit.rate_limit import rate_limit
from twitter_api.resources.api_resources import ApiResources
from twitter_api.types.endpoint import Endpoint
from twitter_api.types.extra_permissive_model import ExtraPermissiveModel
from twitter_api.types.http import downcast_dict
from twitter_api.types.v2_dm_conversation.dm_conversation import DmConversation
from twitter_api.types.v2_dm_conversation.dm_conversation_message import (
    DmConversationMessage,
)
from twitter_api.types.v2_scope import oauth2_scopes
from twitter_api.types.v2_user.user_id import UserId

ENDPOINT = Endpoint(
    "POST", "https://api.twitter.com/2/dm_conversations/with/:participant_id/messages"
)


PostV2DmConversationsWithParticipantMessagesRequestBody = DmConversationMessage


class PostV2DmConversationsWithParticipantMessagesResponseBody(ExtraPermissiveModel):
    data: DmConversation


class PostV2DmConversationsWithParticipantMessagesResources(ApiResources):
    @oauth2_scopes(
        "dm.write",
        "dm.read",
        "tweet.read",
        "users.read",
    )
    @rate_limit(ENDPOINT, "user", requests=200, mins=15)
    @rate_limit(ENDPOINT, "user", requests=1000, hours=24)
    @rate_limit(ENDPOINT, "app", requests=15000, hours=24)
    def post(
        self,
        participant_id: UserId,
        request_body: PostV2DmConversationsWithParticipantMessagesRequestBody,
    ) -> PostV2DmConversationsWithParticipantMessagesResponseBody:
        """
        Direct Message を送る。

        refer: https://developer.twitter.com/en/docs/twitter-api/direct-messages/manage/api-reference/post-dm_conversations-with-participant_id-messages
        """
        return self.request_client.post(
            endpoint=ENDPOINT,
            url=ENDPOINT.url.replace(":participant_id", participant_id),
            body=downcast_dict(request_body),
            response_body_type=PostV2DmConversationsWithParticipantMessagesResponseBody,
        )


class AsyncPostV2DmConversationsWithParticipantMessagesResources(
    PostV2DmConversationsWithParticipantMessagesResources
):
    async def post(
        self,
        participant_id: UserId,
        request_body: PostV2DmConversationsWithParticipantMessagesRequestBody,
    ) -> PostV2DmConversationsWithParticipantMessagesResponseBody:
        return super().post(
            participant_id,
            request_body,
        )
