from typing import NotRequired, Optional, TypedDict

from pydantic import Field

from twitter_api.rate_limit.rate_limit import rate_limit
from twitter_api.resources.api_resources import ApiResources
from twitter_api.types.comma_separatable import CommaSeparatable, comma_separated_str
from twitter_api.types.endpoint import Endpoint
from twitter_api.types.extra_permissive_model import ExtraPermissiveModel
from twitter_api.types.v2_scope import oauth2_scopes
from twitter_api.types.v2_tweet.tweet import Tweet
from twitter_api.types.v2_tweet.tweet_field import TweetField
from twitter_api.types.v2_user.user import User
from twitter_api.types.v2_user.user_expantion import UserExpansion
from twitter_api.types.v2_user.user_field import UserField
from twitter_api.types.v2_user.user_id import UserId

ENDPOINT = Endpoint("GET", "https://api.twitter.com/2/users/:id")

GetV2UserQueryParameters = TypedDict(
    "GetV2UserQueryParameters",
    {
        "expansions": NotRequired[Optional[CommaSeparatable[UserExpansion]]],
        "tweet.fields": NotRequired[Optional[CommaSeparatable[TweetField]]],
        "user.fields": NotRequired[Optional[CommaSeparatable[UserField]]],
    },
)


def _make_query(query: GetV2UserQueryParameters) -> dict:
    return {
        "expansions": comma_separated_str(query.get("expansions")),
        "tweet.fields": comma_separated_str(query.get("tweet.fields")),
        "user.fields": comma_separated_str(query.get("user.fields")),
    }


class GetV2UserResponseBodyIncludes(ExtraPermissiveModel):
    tweets: list[Tweet] = Field(default_factory=list)


class GetV2UserResponseBody(ExtraPermissiveModel):
    data: User
    includes: Optional[GetV2UserResponseBodyIncludes] = None
    errors: Optional[list[dict]] = None


class GetV2UserResources(ApiResources):
    @oauth2_scopes(
        "tweet.read",
        "users.read",
    )
    @rate_limit(ENDPOINT, "app", requests=300, mins=15)
    @rate_limit(ENDPOINT, "user", requests=900, mins=15)
    def get(
        self,
        id: UserId,
        query: Optional[GetV2UserQueryParameters] = None,
    ) -> GetV2UserResponseBody:
        """
        ユーザの情報を取得する。

        refer: https://developer.twitter.com/en/docs/twitter-api/users/lookup/api-reference/get-users-id
        """
        return self.request_client.get(
            endpoint=ENDPOINT,
            url=ENDPOINT.url.replace(":id", id),
            query=_make_query(query) if query is not None else None,
            response_body_type=GetV2UserResponseBody,
        )


class AsyncGetV2UserResources(GetV2UserResources):
    async def get(
        self,
        id: UserId,
        query: Optional[GetV2UserQueryParameters] = None,
    ) -> GetV2UserResponseBody:
        return super().get(id, query)
