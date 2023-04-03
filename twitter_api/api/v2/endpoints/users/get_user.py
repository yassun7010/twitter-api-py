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

ENDPOINT = Endpoint("GET", "https://api.twitter.com/2/users/:id")

V2GetUserQueryParameters = TypedDict(
    "V2GetUserQueryParameters",
    {
        "expansions": NotRequired[Optional[CommaSeparatable[Expansion]]],
        "tweet.fields": NotRequired[Optional[CommaSeparatable[TweetField]]],
        "user.fields": NotRequired[Optional[CommaSeparatable[UserField]]],
    },
)


def _make_query(query: V2GetUserQueryParameters) -> dict:
    return {
        "expansions": comma_separated_str(query.get("expansions")),
        "tweet.fields": comma_separated_str(query.get("tweet.fields")),
        "user.fields": comma_separated_str(query.get("user.fields")),
    }


class V2GetUserResponseBodyIncludes(ExtraPermissiveModel):
    tweets: list[Tweet]


class V2GetUserResponseBody(ExtraPermissiveModel):
    data: User
    includes: Optional[V2GetUserResponseBodyIncludes] = None


class V2GetUserResources(ApiResources):
    @rate_limit(ENDPOINT, "app", requests=300, mins=15)
    @rate_limit(ENDPOINT, "user", requests=900, mins=15)
    def get(
        self,
        id: UserId,
        query: Optional[V2GetUserQueryParameters] = None,
    ) -> V2GetUserResponseBody:
        # flake8: noqa E501
        """
        ユーザの情報を取得する。

        refer: https://developer.twitter.com/en/docs/twitter-api/users/lookup/api-reference/get-users-id
        """
        return self.request_client.get(
            endpoint=ENDPOINT,
            url=ENDPOINT.url.replace(":id", id),
            query=_make_query(query) if query is not None else None,
            response_type=V2GetUserResponseBody,
        )
