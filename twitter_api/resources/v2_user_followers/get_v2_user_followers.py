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
from twitter_api.types.v2_scope import oauth2_scopes
from twitter_api.types.v2_tweet.tweet import Tweet
from twitter_api.types.v2_tweet.tweet_field import TweetField
from twitter_api.types.v2_user.user import User
from twitter_api.types.v2_user.user_expantion import UserExpansion
from twitter_api.types.v2_user.user_field import UserField
from twitter_api.types.v2_user.user_id import UserId

ENDPOINT = Endpoint("GET", "https://api.twitter.com/2/users/:id/followers")

GetV2UserFollowersQueryParameters = TypedDict(
    "GetV2UserFollowersQueryParameters",
    {
        "expansions": NotRequired[Optional[CommaSeparatable[UserExpansion]]],
        "pagination_token": NotRequired[Optional[str]],
        "max_results": NotRequired[Optional[int]],
        "tweet.fields": NotRequired[Optional[CommaSeparatable[TweetField]]],
        "user.fields": NotRequired[Optional[CommaSeparatable[UserField]]],
    },
)


def _make_query(query: GetV2UserFollowersQueryParameters) -> dict:
    return {
        "expansions": comma_separated_str(query.get("expansions")),
        "pagination_token": query.get("pagination_token"),
        "max_results": query.get("max_results"),
        "tweet.fields": comma_separated_str(query.get("tweet.fields")),
        "user.fields": comma_separated_str(query.get("user.fields")),
    }


class GetV2UserFollowersResponseBodyMeta(ExtraPermissiveModel):
    result_count: int
    next_token: Optional[PaginationToken] = None
    previous_token: Optional[PaginationToken] = None

    def extend(self, other: Self) -> None:
        self.result_count += other.result_count
        self.next_token = None
        self.previous_token = None


class GetV2UserFollowersResponseBodyIncludes(ExtraPermissiveModel):
    tweets: list[Tweet] = Field(default_factory=list)

    def extend(self, other: Self) -> None:
        self.tweets.extend(other.tweets)


class GetV2UserFollowersResponseBody(ExtraPermissiveModel, PageResponseBody):
    data: list[User] = Field(default_factory=list)
    meta: GetV2UserFollowersResponseBodyMeta
    includes: GetV2UserFollowersResponseBodyIncludes = Field(
        default_factory=GetV2UserFollowersResponseBodyIncludes,
    )
    errors: Optional[list[dict]] = None

    @property
    def meta_next_token(self) -> Optional[PaginationToken]:
        return self.meta.next_token

    def extend(self, other: Self) -> None:
        self.data.extend(other.data)
        self.meta.extend(other.meta)
        self.includes.extend(other.includes)

        if other.errors is not None:
            if self.errors is not None:
                self.errors.extend(other.errors)
            else:
                self.errors = other.errors


class GetV2UserFollowersResources(ApiResources):
    @oauth2_scopes(
        "tweet.read",
        "users.read",
        "follows.read",
    )
    @rate_limit(ENDPOINT, "app", requests=15, mins=15)
    @rate_limit(ENDPOINT, "user", requests=15, mins=15)
    def get(
        self,
        id: UserId,
        query: Optional[GetV2UserFollowersQueryParameters] = None,
    ) -> GetV2UserFollowersResponseBody:
        """
        ユーザのフォロワーの一覧を取得する。

        refer: https://developer.twitter.com/en/docs/twitter-api/users/follows/api-reference/get-users-id-followers
        """
        return self.request_client.get(
            endpoint=ENDPOINT,
            url=ENDPOINT.url.replace(":id", id),
            query=_make_query(query) if query is not None else None,
            response_body_type=GetV2UserFollowersResponseBody,
        )

    def get_paging_response_body_iter(
        self,
        id: UserId,
        query: Optional[GetV2UserFollowersQueryParameters] = None,
    ) -> Generator[GetV2UserFollowersResponseBody, None, None]:
        """
        ユーザのフォロワーの一覧を取得する。

        ページングされた API のレスポンスをイテレータで返す。

        refer: https://developer.twitter.com/en/docs/twitter-api/users/follows/api-reference/get-users-id-followers
        """
        return get_paging_response_body_iter_sync(
            partial(self.get, id), query, "pagination_token"
        )

    def get_collected_paging_response_body(
        self,
        id: UserId,
        query: Optional[GetV2UserFollowersQueryParameters] = None,
    ) -> GetV2UserFollowersResponseBody:
        """
        ユーザのフォロワーの一覧を取得する。

        ページングされた API のレスポンスをまとめて一つのレスポンスとして返す。

        refer: https://developer.twitter.com/en/docs/twitter-api/users/follows/api-reference/get-users-id-followers
        """
        return get_collected_paging_response_body_sync(
            partial(self.get, id), query, "pagination_token"
        )


class AsyncGetV2UserFollowersResources(GetV2UserFollowersResources):
    async def get(
        self,
        id: UserId,
        query: Optional[GetV2UserFollowersQueryParameters] = None,
    ) -> GetV2UserFollowersResponseBody:
        return super().get(id, query)

    async def get_paging_response_body_iter(
        self,
        id: UserId,
        query: Optional[GetV2UserFollowersQueryParameters] = None,
    ) -> AsyncGenerator[GetV2UserFollowersResponseBody, None]:
        return get_paging_response_body_iter_async(
            partial(self.get, id), query, "pagination_token"
        )

    async def get_collected_paging_response_body(
        self,
        id: UserId,
        query: Optional[GetV2UserFollowersQueryParameters] = None,
    ) -> GetV2UserFollowersResponseBody:
        return await get_collected_paging_response_body_async(
            partial(self.get, id), query, "pagination_token"
        )
