from datetime import datetime
from typing import NotRequired, Optional, Self, TypedDict

from twitter_api.api.resources.api_resources import ApiResources
from twitter_api.api.types.v2_dm_conversation.dm_conversation_id import DmConversationId
from twitter_api.api.types.v2_dm_event.dm_event_field import DmEventField
from twitter_api.api.types.v2_dm_event.dm_event_id import DmEventId
from twitter_api.api.types.v2_dm_event.dm_event_type import DmEventType
from twitter_api.api.types.v2_expansion import Expansion
from twitter_api.api.types.v2_media.media_key import MediaKey
from twitter_api.api.types.v2_scope import oauth2_scopes
from twitter_api.api.types.v2_tweet.tweet_field import TweetField
from twitter_api.api.types.v2_user.user_field import UserField
from twitter_api.api.types.v2_user.user_id import UserId
from twitter_api.rate_limit.rate_limit import rate_limit
from twitter_api.types.comma_separatable import CommaSeparatable, comma_separated_str
from twitter_api.types.endpoint import Endpoint
from twitter_api.types.extra_permissive_model import ExtraPermissiveModel

ENDPOINT = Endpoint(
    "GET",
    "https://api.twitter.com/2/dm_conversations/with/:participant_id/dm_events",
)


GetV2DmConversationsWithParticipantDmEventsQueryParameters = TypedDict(
    "GetV2DmConversationsWithParticipantDmEventsQueryParameters",
    {
        "dm_event.fields": NotRequired[Optional[CommaSeparatable[DmEventField]]],
        "event_type": NotRequired[Optional[DmEventType]],
        "expansions": NotRequired[Optional[Expansion]],
        "max_results": NotRequired[Optional[int]],
        "pagination_token": NotRequired[Optional[str]],
        "tweet.fields": NotRequired[Optional[CommaSeparatable[TweetField]]],
        "user.fields": NotRequired[Optional[CommaSeparatable[UserField]]],
    },
)


def _make_query(
    query: GetV2DmConversationsWithParticipantDmEventsQueryParameters,
) -> dict:
    return {
        "dm_event.fields": comma_separated_str(query.get("dm_event.fields")),
        "event_type": query.get("event_type"),
        "expansions": comma_separated_str(query.get("expansions")),
        "max_results": query.get("max_results"),
        "pagination_token": query.get("pagination_token"),
        "tweet.fields": comma_separated_str(query.get("tweet.fields")),
        "user.fields": comma_separated_str(query.get("user.fields")),
    }


class GetV2DmConversationsWithParticipantDmEventsResponseBodyDataAttachments(
    ExtraPermissiveModel
):
    media_keys: list[MediaKey]


class GetV2DmConversationsWithParticipantDmEventsResponseBodyData(ExtraPermissiveModel):
    id: DmEventId
    text: str
    event_type: DmEventType
    created_at: datetime
    sender_id: UserId
    dm_conversation_id: DmConversationId
    attachments: Optional[
        GetV2DmConversationsWithParticipantDmEventsResponseBodyDataAttachments
    ] = None


class GetV2DmConversationsWithParticipantDmEventsResponseBodyMeta(ExtraPermissiveModel):
    result_count: int
    next_token: Optional[str] = None
    previous_token: Optional[str] = None

    def extend(self, other: Self) -> None:
        self.result_count += other.result_count
        self.next_token = None
        self.previous_token = None


class GetV2DmConversationsWithParticipantDmEventsResponseBody(ExtraPermissiveModel):
    data: list[GetV2DmConversationsWithParticipantDmEventsResponseBodyData]
    meta: GetV2DmConversationsWithParticipantDmEventsResponseBodyMeta
    errors: Optional[list[dict]] = None


class GetV2DmConversationsWithParticipantDmEventsResources(ApiResources):
    @oauth2_scopes(
        "dm.read",
        "tweet.read",
        "users.read",
    )
    @rate_limit(ENDPOINT, "user", requests=300, mins=15)
    def get(
        self,
        participant_id: UserId,
        query: GetV2DmConversationsWithParticipantDmEventsQueryParameters,
    ) -> GetV2DmConversationsWithParticipantDmEventsResponseBody:
        """
        DM の参加者のイベント情報を返す。

        refer: https://developer.twitter.com/en/docs/twitter-api/direct-messages/lookup/api-reference/get-dm_conversations-with-participant_id-dm_events
        """
        return self.request_client.get(
            endpoint=ENDPOINT,
            url=ENDPOINT.url.replace(":participant_id", participant_id),
            query=_make_query(query) if query is not None else None,
            response_body_type=GetV2DmConversationsWithParticipantDmEventsResponseBody,
        )


class AsyncGetV2DmConversationsWithParticipantDmEventsResources(
    GetV2DmConversationsWithParticipantDmEventsResources
):
    async def post(
        self,
        participant_id: UserId,
        query: GetV2DmConversationsWithParticipantDmEventsQueryParameters,
    ) -> GetV2DmConversationsWithParticipantDmEventsResponseBody:
        return super().get(
            participant_id,
            query,
        )
