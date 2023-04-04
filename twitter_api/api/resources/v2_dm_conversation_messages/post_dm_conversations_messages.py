from twitter_api.api.resources.api_resources import ApiResources
from twitter_api.api.types.v2_dm_conversation.dm_conversation_id import DmConversationId
from twitter_api.api.types.v2_dm_conversation.dm_conversation_message import (
    DmConversationMessage,
)
from twitter_api.api.types.v2_dm_event.dm_event_id import DmEventId
from twitter_api.rate_limit.rate_limit_decorator import rate_limit
from twitter_api.types.endpoint import Endpoint
from twitter_api.types.extra_permissive_model import ExtraPermissiveModel
from twitter_api.types.http import downcast_dict

ENDPOINT = Endpoint(
    "POST", "https://api.twitter.com/2/dm_conversations/:dm_conversation_id/messages"
)


V2PostDmConversationMessagesRequestBody = DmConversationMessage


class V2PostDmConversationMessagesResponseBody(ExtraPermissiveModel):
    dm_conversation_id: DmConversationId
    dm_event_id: DmEventId


class V2PostDmConversationMessagesResources(ApiResources):
    @rate_limit(ENDPOINT, "user", requests=200, mins=15)
    @rate_limit(ENDPOINT, "user", requests=1000, hours=24)
    @rate_limit(ENDPOINT, "app", requests=15000, hours=24)
    def post(
        self,
        dm_conversation_id: DmConversationId,
        request_body: V2PostDmConversationMessagesRequestBody,
    ) -> V2PostDmConversationMessagesResponseBody:
        # flake8: noqa E501
        """
        指定した会話に Direct Message を送る。

        refer: https://developer.twitter.com/en/docs/twitter-api/direct-messages/manage/api-reference/post-dm_conversations-dm_conversation_id-messages
        """
        return self.request_client.post(
            endpoint=ENDPOINT,
            url=ENDPOINT.url.replace(":dm_conversation_id", dm_conversation_id),
            json=downcast_dict(request_body),
            response_type=V2PostDmConversationMessagesResponseBody,
        )
