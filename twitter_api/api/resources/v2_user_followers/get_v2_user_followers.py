from typing import NotRequired, Optional, TypedDict

from pydantic import Field

from twitter_api.api.resources.api_resources import ApiResources
from twitter_api.api.types.v2_expansion import Expansion
from twitter_api.api.types.v2_scope import oauth2_scopes
from twitter_api.api.types.v2_tweet.tweet import Tweet
from twitter_api.api.types.v2_tweet.tweet_field import TweetField
from twitter_api.api.types.v2_user.user import User
from twitter_api.api.types.v2_user.user_field import UserField
from twitter_api.api.types.v2_user.user_id import UserId
from twitter_api.rate_limit.rate_limit_decorator import rate_limit
from twitter_api.types.comma_separatable import CommaSeparatable, comma_separated_str
from twitter_api.types.endpoint import Endpoint
from twitter_api.types.extra_permissive_model import ExtraPermissiveModel

ENDPOINT = Endpoint("GET", "https://api.twitter.com/2/users/:id/followers")

GetV2UserFollowersQueryParameters = TypedDict(
    "GetV2UserFollowersQueryParameters",
    {
        "expansions": NotRequired[Optional[CommaSeparatable[Expansion]]],
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
    previous_token: Optional[str] = None
    next_token: Optional[str] = None


class GetV2UserFollowersResponseBodyIncludes(ExtraPermissiveModel):
    tweets: list[Tweet] = Field(default_factory=list)


class GetV2UserFollowersResponseBody(ExtraPermissiveModel):
    data: list[User]
    meta: GetV2UserFollowersResponseBodyMeta
    includes: Optional[GetV2UserFollowersResponseBodyIncludes] = None
    errors: Optional[list[dict]] = None


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
            response_type=GetV2UserFollowersResponseBody,
        )


class AsyncGetV2UserFollowersResources(GetV2UserFollowersResources):
    async def get(
        self,
        id: UserId,
        query: Optional[GetV2UserFollowersQueryParameters] = None,
    ) -> GetV2UserFollowersResponseBody:
        return super().get(id, query)
