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
from twitter_api.types.v2_media.media import Media
from twitter_api.types.v2_media.media_field import MediaField
from twitter_api.types.v2_place.place import Place
from twitter_api.types.v2_place.place_field import PlaceField
from twitter_api.types.v2_poll.poll import Poll
from twitter_api.types.v2_poll.poll_field import PollField
from twitter_api.types.v2_scope import oauth2_scopes
from twitter_api.types.v2_tweet.tweet import Tweet
from twitter_api.types.v2_tweet.tweet_field import TweetField
from twitter_api.types.v2_user.user import User
from twitter_api.types.v2_user.user_expantion import UserExpansion
from twitter_api.types.v2_user.user_field import UserField
from twitter_api.types.v2_user.user_id import UserId

ENDPOINT = Endpoint("GET", "https://api.twitter.com/2/users/:id/liked_tweets")

GetV2UserLikedTweetsQueryParameters = TypedDict(
    "GetV2UserLikedTweetsQueryParameters",
    {
        "expansions": NotRequired[Optional[CommaSeparatable[UserExpansion]]],
        "pagination_token": NotRequired[Optional[str]],
        "max_results": NotRequired[Optional[int]],
        "media.fields": NotRequired[Optional[CommaSeparatable[MediaField]]],
        "place.fields": NotRequired[Optional[CommaSeparatable[PlaceField]]],
        "poll.fields": NotRequired[Optional[CommaSeparatable[PollField]]],
        "tweet.fields": NotRequired[Optional[CommaSeparatable[TweetField]]],
        "user.fields": NotRequired[Optional[CommaSeparatable[UserField]]],
    },
)


def _make_query(query: GetV2UserLikedTweetsQueryParameters) -> dict:
    return {
        "expansions": comma_separated_str(query.get("expansions")),
        "pagination_token": query.get("pagination_token"),
        "max_results": query.get("max_results"),
        "media.fields": comma_separated_str(query.get("media.fields")),
        "place.fields": comma_separated_str(query.get("place.fields")),
        "poll.fields": comma_separated_str(query.get("poll.fields")),
        "tweet.fields": comma_separated_str(query.get("tweet.fields")),
        "user.fields": comma_separated_str(query.get("user.fields")),
    }


class GetV2UserLikedTweetsResponseBodyIncludes(ExtraPermissiveModel):
    users: list[User] = Field(default_factory=list)
    tweets: list[Tweet] = Field(default_factory=list)
    places: list[Place] = Field(default_factory=list)
    media: list[Media] = Field(default_factory=list)
    polls: list[Poll] = Field(default_factory=list)

    def extend(self, other: Self) -> None:
        self.users.extend(other.users)
        self.tweets.extend(other.tweets)
        self.places.extend(other.places)
        self.media.extend(other.media)
        self.polls.extend(other.polls)


class GetV2UserLikedTweetsResponseBodyMeta(ExtraPermissiveModel):
    result_count: int
    next_token: Optional[PaginationToken] = None
    previous_token: Optional[PaginationToken] = None

    def extend(self, other: Self) -> None:
        self.result_count += other.result_count
        self.next_token = None
        self.previous_token = None


class GetV2UserLikedTweetsResponseBody(ExtraPermissiveModel, PageResponseBody):
    data: list[Tweet] = Field(default_factory=list)
    meta: Optional[GetV2UserLikedTweetsResponseBodyMeta] = None
    includes: GetV2UserLikedTweetsResponseBodyIncludes = Field(
        default_factory=GetV2UserLikedTweetsResponseBodyIncludes,
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


class GetV2UserLikedTweetsResources(ApiResources):
    @oauth2_scopes(
        "tweet.read",
        "users.read",
        "like.read",
    )
    @rate_limit(ENDPOINT, "app", requests=75, mins=15)
    @rate_limit(ENDPOINT, "user", requests=75, mins=15)
    def get(
        self,
        id: UserId,
        query: Optional[GetV2UserLikedTweetsQueryParameters] = None,
    ) -> GetV2UserLikedTweetsResponseBody:
        """
        ユーザが「いいね」をしているツイートの一覧を取得する。

        refer: https://developer.twitter.com/en/docs/twitter-api/tweets/likes/api-reference/get-users-id-liked_tweets
        """
        return self.request_client.get(
            endpoint=ENDPOINT,
            url=ENDPOINT.url.replace(":id", id),
            query=_make_query(query) if query is not None else None,
            response_body_type=GetV2UserLikedTweetsResponseBody,
        )

    def get_paging_response_body_iter(
        self,
        id: UserId,
        query: Optional[GetV2UserLikedTweetsQueryParameters] = None,
    ) -> Generator[GetV2UserLikedTweetsResponseBody, None, None]:
        """
        ユーザが「いいね」をしているツイートの一覧を取得する。

        ページングされた API のレスポンスをイテレータで返す。

        refer: https://developer.twitter.com/en/docs/twitter-api/tweets/likes/api-reference/get-users-id-liked_tweets
        """
        return get_paging_response_body_iter_sync(
            partial(self.get, id), query, "pagination_token"
        )

    def get_collected_paging_response_body(
        self,
        id: UserId,
        query: Optional[GetV2UserLikedTweetsQueryParameters] = None,
    ) -> GetV2UserLikedTweetsResponseBody:
        """
        ユーザが「いいね」をしているツイートの一覧を取得する。

        ページングされた API のレスポンスをまとめて一つのレスポンスとして返す。

        refer: https://developer.twitter.com/en/docs/twitter-api/tweets/likes/api-reference/get-users-id-liked_tweets
        """
        return get_collected_paging_response_body_sync(
            partial(self.get, id), query, "pagination_token"
        )


class AsyncGetV2UserLikedTweetsResources(GetV2UserLikedTweetsResources):
    async def get(
        self,
        id: UserId,
        query: Optional[GetV2UserLikedTweetsQueryParameters] = None,
    ) -> GetV2UserLikedTweetsResponseBody:
        return super().get(id, query)

    async def get_paging_response_body_iter(
        self,
        id: UserId,
        query: Optional[GetV2UserLikedTweetsQueryParameters] = None,
    ) -> AsyncGenerator[GetV2UserLikedTweetsResponseBody, None]:
        return get_paging_response_body_iter_async(
            partial(self.get, id), query, "pagination_token"
        )

    async def get_collected_paging_response_body(
        self,
        id: UserId,
        query: Optional[GetV2UserLikedTweetsQueryParameters] = None,
    ) -> GetV2UserLikedTweetsResponseBody:
        return await get_collected_paging_response_body_async(
            partial(self.get, id), query, "pagination_token"
        )
