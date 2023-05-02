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

ENDPOINT = Endpoint("GET", "https://api.twitter.com/2/users")

GetV2UsersQueryParameters = TypedDict(
    "GetV2UsersQueryParameters",
    {
        "ids": CommaSeparatable[UserId],
        "expansions": NotRequired[Optional[CommaSeparatable[UserExpansion]]],
        "tweet.fields": NotRequired[Optional[CommaSeparatable[TweetField]]],
        "user.fields": NotRequired[Optional[CommaSeparatable[UserField]]],
    },
)


def _make_query(query: GetV2UsersQueryParameters) -> dict:
    return {
        "ids": comma_separated_str(query["ids"]),
        "expansions": comma_separated_str(query.get("expansions")),
        "tweet.fields": comma_separated_str(query.get("tweet.fields")),
        "user.fields": comma_separated_str(query.get("user.fields")),
    }


class GetV2UsersResponseBodyIncludes(ExtraPermissiveModel):
    tweets: list[Tweet] = Field(default_factory=list)


class GetV2UsersResponseBody(ExtraPermissiveModel):
    data: list[User]
    includes: Optional[GetV2UsersResponseBodyIncludes] = None
    errors: Optional[list[dict]] = None


class GetV2UsersResources(ApiResources):
    @oauth2_scopes(
        "tweet.read",
        "users.read",
    )
    @rate_limit(ENDPOINT, "app", requests=300, mins=15)
    @rate_limit(ENDPOINT, "user", requests=900, mins=15)
    def get(self, query: GetV2UsersQueryParameters) -> GetV2UsersResponseBody:
        """
        ユーザの一覧を取得する。

        refer: https://developer.twitter.com/en/docs/twitter-api/users/lookup/api-reference/get-users
        """
        return self.request_client.get(
            endpoint=ENDPOINT,
            query=_make_query(query),
            response_body_type=GetV2UsersResponseBody,
        )


class AsyncGetV2UsersResources(GetV2UsersResources):
    async def get(self, query: GetV2UsersQueryParameters) -> GetV2UsersResponseBody:
        return super().get(query)
