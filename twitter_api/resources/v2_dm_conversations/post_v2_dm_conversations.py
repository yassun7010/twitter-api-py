from typing import Literal, TypedDict

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

ENDPOINT = Endpoint("POST", "https://api.twitter.com/2/dm_conversations")


PostV2DmConversationsRequestBody = TypedDict(
    "PostV2DmConversationsRequestBody",
    {
        "conversation_type": Literal["Group"],
        "message": DmConversationMessage,
        "participant_ids": list[UserId],
    },
)


class PostV2DmConversationsResponseBody(ExtraPermissiveModel):
    data: DmConversation


class PostV2DmConversationsResources(ApiResources):
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
        request_body: PostV2DmConversationsRequestBody,
    ) -> PostV2DmConversationsResponseBody:
        """
        DM 用の新しい会話グループを作成する。

        refer: https://developer.twitter.com/en/docs/twitter-api/direct-messages/manage/api-reference/post-dm_conversations
        """
        return self.request_client.post(
            endpoint=ENDPOINT,
            body=downcast_dict(request_body),
            response_body_type=PostV2DmConversationsResponseBody,
        )


class AsyncPostV2DmConversationsResources(PostV2DmConversationsResources):
    async def post(
        self,
        request_body: PostV2DmConversationsRequestBody,
    ) -> PostV2DmConversationsResponseBody:
        return super().post(
            request_body,
        )
