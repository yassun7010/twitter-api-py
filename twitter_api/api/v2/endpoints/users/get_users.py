from typing import NotRequired, Optional, TypedDict

from twitter_api.api.api_resources import ApiResources
from twitter_api.api.v2.types.expansion import Expansion
from twitter_api.api.v2.types.tweet.tweet import Tweet
from twitter_api.api.v2.types.tweet.tweet_field import TweetField
from twitter_api.api.v2.types.user.user import User
from twitter_api.api.v2.types.user.user_field import UserField
from twitter_api.api.v2.types.user.user_id import UserId
from twitter_api.rate_limit.rate_limit_decorator import rate_limit
from twitter_api.types.comma_separatable import CommaSeparatable, comma_separated_str
from twitter_api.types.endpoint import Endpoint
from twitter_api.types.extra_permissive_model import ExtraPermissiveModel

ENDPOINT = Endpoint("GET", "https://api.twitter.com/2/users")

V2GetUsersQueryParameters = TypedDict(
    "V2GetUsersQueryParameters",
    {
        "ids": CommaSeparatable[UserId],
        "expansions": NotRequired[Optional[CommaSeparatable[Expansion]]],
        "tweet.fields": NotRequired[Optional[CommaSeparatable[TweetField]]],
        "user.fields": NotRequired[Optional[CommaSeparatable[UserField]]],
    },
)


def _make_query(query: V2GetUsersQueryParameters) -> dict:
    return {
        "ids": comma_separated_str(query["ids"]),
        "expansions": comma_separated_str(query.get("expansions")),
        "tweet.fields": comma_separated_str(query.get("tweet.fields")),
        "user.fields": comma_separated_str(query.get("user.fields")),
    }


class V2GetUsersResponseBodyIncludes(ExtraPermissiveModel):
    tweets: list[Tweet]


class V2GetUsersResponseBody(ExtraPermissiveModel):
    data: list[User]
    includes: Optional[V2GetUsersResponseBodyIncludes] = None


class V2GetUsersResources(ApiResources):
    @rate_limit(ENDPOINT, "app", requests=300, mins=15)
    @rate_limit(ENDPOINT, "user", requests=900, mins=15)
    def get(self, query: V2GetUsersQueryParameters) -> V2GetUsersResponseBody:
        # flake8: noqa E501
        """
        ユーザの一覧を取得する。

        refer: https://developer.twitter.com/en/docs/twitter-api/users/lookup/api-reference/get-users
        """
        return self.request_client.get(
            endpoint=ENDPOINT,
            query=_make_query(query),
            response_type=V2GetUsersResponseBody,
        )
