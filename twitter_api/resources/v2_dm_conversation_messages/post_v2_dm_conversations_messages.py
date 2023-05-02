from twitter_api.rate_limit.rate_limit import rate_limit
from twitter_api.resources.api_resources import ApiResources
from twitter_api.types.endpoint import Endpoint
from twitter_api.types.extra_permissive_model import ExtraPermissiveModel
from twitter_api.types.http import downcast_dict
from twitter_api.types.v2_dm_conversation.dm_conversation import DmConversation
from twitter_api.types.v2_dm_conversation.dm_conversation_id import DmConversationId
from twitter_api.types.v2_dm_conversation.dm_conversation_message import (
    DmConversationMessage,
)
from twitter_api.types.v2_scope import oauth2_scopes

ENDPOINT = Endpoint(
    "POST", "https://api.twitter.com/2/dm_conversations/:dm_conversation_id/messages"
)


PostV2DmConversationMessagesRequestBody = DmConversationMessage


class PostV2DmConversationMessagesResponseBody(ExtraPermissiveModel):
    data: DmConversation


class PostV2DmConversationMessagesResources(ApiResources):
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
        dm_conversation_id: DmConversationId,
        request_body: PostV2DmConversationMessagesRequestBody,
    ) -> PostV2DmConversationMessagesResponseBody:
        """
        指定した会話に Direct Message を送る。

        refer: https://developer.twitter.com/en/docs/twitter-api/direct-messages/manage/api-reference/post-dm_conversations-dm_conversation_id-messages
        """
        return self.request_client.post(
            endpoint=ENDPOINT,
            url=ENDPOINT.url.replace(":dm_conversation_id", dm_conversation_id),
            body=downcast_dict(request_body),
            response_body_type=PostV2DmConversationMessagesResponseBody,
        )


class AsyncPostV2DmConversationMessagesResources(PostV2DmConversationMessagesResources):
    async def post(
        self,
        dm_conversation_id: DmConversationId,
        request_body: PostV2DmConversationMessagesRequestBody,
    ) -> PostV2DmConversationMessagesResponseBody:
        return super().post(
            dm_conversation_id,
            request_body,
        )
