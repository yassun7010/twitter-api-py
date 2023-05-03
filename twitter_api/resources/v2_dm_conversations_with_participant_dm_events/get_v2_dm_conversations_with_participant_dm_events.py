from datetime import datetime
from functools import partial
from typing import AsyncGenerator, Generator, NotRequired, Optional, Self, TypedDict

from pydantic import Field

from twitter_api.rate_limit.rate_limit import rate_limit
from twitter_api.resources.api_resources import ApiResources
from twitter_api.types._paging import (
    PageResponseBody,
    get_collected_paging_response_body_async,
    get_collected_paging_response_body_sync,
    get_paging_response_body_iter_async,
    get_paging_response_body_iter_sync,
)
from twitter_api.types.comma_separatable import CommaSeparatable, comma_separated_str
from twitter_api.types.endpoint import Endpoint
from twitter_api.types.extra_permissive_model import ExtraPermissiveModel
from twitter_api.types.pagination_token import PaginationToken
from twitter_api.types.v2_dm_conversation.dm_conversation_id import DmConversationId
from twitter_api.types.v2_dm_event.dm_event_expansion import DmEventExpansion
from twitter_api.types.v2_dm_event.dm_event_field import DmEventField
from twitter_api.types.v2_dm_event.dm_event_id import DmEventId
from twitter_api.types.v2_dm_event.dm_event_type import DmEventType
from twitter_api.types.v2_media.media_key import MediaKey
from twitter_api.types.v2_scope import oauth2_scopes
from twitter_api.types.v2_tweet.tweet_field import TweetField
from twitter_api.types.v2_user.user import User
from twitter_api.types.v2_user.user_field import UserField
from twitter_api.types.v2_user.user_id import UserId

ENDPOINT = Endpoint(
    "GET",
    "https://api.twitter.com/2/dm_conversations/with/:participant_id/dm_events",
)


GetV2DmConversationsWithParticipantDmEventsQueryParameters = TypedDict(
    "GetV2DmConversationsWithParticipantDmEventsQueryParameters",
    {
        "dm_event.fields": NotRequired[Optional[CommaSeparatable[DmEventField]]],
        "event_types": NotRequired[Optional[CommaSeparatable[DmEventType]]],
        "expansions": NotRequired[Optional[CommaSeparatable[DmEventExpansion]]],
        "max_results": NotRequired[Optional[int]],
        "pagination_token": NotRequired[Optional[PaginationToken]],
        "tweet.fields": NotRequired[Optional[CommaSeparatable[TweetField]]],
        "user.fields": NotRequired[Optional[CommaSeparatable[UserField]]],
    },
)


def _make_query(
    query: GetV2DmConversationsWithParticipantDmEventsQueryParameters,
) -> dict:
    return {
        "dm_event.fields": comma_separated_str(query.get("dm_event.fields")),
        "event_types": comma_separated_str(query.get("event_types")),
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
    created_at: Optional[datetime] = None
    sender_id: Optional[UserId] = None
    dm_conversation_id: Optional[DmConversationId] = None
    attachments: Optional[
        GetV2DmConversationsWithParticipantDmEventsResponseBodyDataAttachments
    ] = None


class GetV2DmConversationsWithParticipantDmEventsResponseBodyMeta(ExtraPermissiveModel):
    result_count: int
    next_token: Optional[PaginationToken] = None
    previous_token: Optional[PaginationToken] = None

    def extend(self, other: Self) -> None:
        self.result_count += other.result_count
        self.next_token = None
        self.previous_token = None


class GetV2DmConversationsWithParticipantDmEventsResponseBodyIncludes(
    ExtraPermissiveModel
):
    users: list[User] = Field(default_factory=list)

    def extend(self, other: Self) -> None:
        self.users.extend(other.users)


class GetV2DmConversationsWithParticipantDmEventsResponseBody(
    ExtraPermissiveModel,
    PageResponseBody,
):
    data: list[GetV2DmConversationsWithParticipantDmEventsResponseBodyData] = Field(
        default_factory=list
    )
    meta: GetV2DmConversationsWithParticipantDmEventsResponseBodyMeta
    includes: GetV2DmConversationsWithParticipantDmEventsResponseBodyIncludes = Field(
        default_factory=GetV2DmConversationsWithParticipantDmEventsResponseBodyIncludes,
    )
    errors: Optional[list[dict]] = None

    @property
    def meta_next_token(self) -> Optional[PaginationToken]:
        if self.meta is None:
            return None

        return self.meta.next_token

    def extend(self, other: Self) -> None:
        self.data.extend(other.data)
        self.includes.extend(other.includes)

        if self.meta is not None and other.meta is not None:
            self.meta.extend(other.meta)

        if other.errors is not None:
            if self.errors is not None:
                self.errors.extend(other.errors)
            else:
                self.errors = other.errors


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
        query: Optional[
            GetV2DmConversationsWithParticipantDmEventsQueryParameters
        ] = None,
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

    def get_paging_response_body_iter(
        self,
        participant_id: UserId,
        query: Optional[
            GetV2DmConversationsWithParticipantDmEventsQueryParameters
        ] = None,
    ) -> Generator[GetV2DmConversationsWithParticipantDmEventsResponseBody, None, None]:
        """
        DM の参加者のイベント情報を返す。

        ページングされた API のレスポンスをイテレータで返す。

        refer: https://developer.twitter.com/en/docs/twitter-api/tweets/likes/api-reference/get-users-participant_id-liked_tweets
        """
        return get_paging_response_body_iter_sync(
            partial(self.get, participant_id), query, "pagination_token"
        )

    def get_collected_paging_response_body(
        self,
        participant_id: UserId,
        query: Optional[
            GetV2DmConversationsWithParticipantDmEventsQueryParameters
        ] = None,
    ) -> GetV2DmConversationsWithParticipantDmEventsResponseBody:
        """
        DM の参加者のイベント情報を返す。

        ページングされた API のレスポンスをまとめて一つのレスポンスとして返す。

        refer: https://developer.twitter.com/en/docs/twitter-api/tweets/likes/api-reference/get-users-participant_id-liked_tweets
        """
        return get_collected_paging_response_body_sync(
            partial(self.get, participant_id), query, "pagination_token"
        )


class AsyncGetV2DmConversationsWithParticipantDmEventsResources(
    GetV2DmConversationsWithParticipantDmEventsResources
):
    async def get(
        self,
        participant_id: UserId,
        query: Optional[
            GetV2DmConversationsWithParticipantDmEventsQueryParameters
        ] = None,
    ) -> GetV2DmConversationsWithParticipantDmEventsResponseBody:
        return super().get(
            participant_id,
            query,
        )

    async def get_paging_response_body_iter(
        self,
        participant_id: UserId,
        query: Optional[
            GetV2DmConversationsWithParticipantDmEventsQueryParameters
        ] = None,
    ) -> AsyncGenerator[GetV2DmConversationsWithParticipantDmEventsResponseBody, None]:
        return get_paging_response_body_iter_async(
            partial(self.get, participant_id), query, "pagination_token"
        )

    async def get_collected_paging_response_body(
        self,
        participant_id: UserId,
        query: Optional[
            GetV2DmConversationsWithParticipantDmEventsQueryParameters
        ] = None,
    ) -> GetV2DmConversationsWithParticipantDmEventsResponseBody:
        return await get_collected_paging_response_body_async(
            partial(self.get, participant_id), query, "pagination_token"
        )
