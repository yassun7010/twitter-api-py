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

ENDPOINT = Endpoint("GET", "https://api.twitter.com/2/users/:id/followers")

V2GetUserFollowersQueryParameters = TypedDict(
    "V2GetUserFollowersQueryParameters",
    {
        "expansions": NotRequired[Optional[CommaSeparatable[Expansion]]],
        "pagination_token": NotRequired[Optional[str]],
        "max_results": NotRequired[Optional[int]],
        "tweet.fields": NotRequired[Optional[CommaSeparatable[TweetField]]],
        "user.fields": NotRequired[Optional[CommaSeparatable[UserField]]],
    },
)


def _make_query(query: V2GetUserFollowersQueryParameters) -> dict:
    return {
        "expansions": comma_separated_str(query.get("expansions")),
        "pagination_token": query.get("pagination_token"),
        "max_results": query.get("max_results"),
        "tweet.fields": comma_separated_str(query.get("tweet.fields")),
        "user.fields": comma_separated_str(query.get("user.fields")),
    }


class V2GetUserFollowersResponseBodyMeta(ExtraPermissiveModel):
    result_count: int
    previous_token: Optional[str] = None
    next_token: Optional[str] = None


class V2GetUserFollowersResponseBodyIncludes(ExtraPermissiveModel):
    tweets: list[Tweet]


class V2GetUserFollowersResponseBody(ExtraPermissiveModel):
    data: list[User]
    meta: V2GetUserFollowersResponseBodyMeta
    includes: Optional[V2GetUserFollowersResponseBodyIncludes] = None


class V2GetUserFollowersResources(ApiResources):
    @rate_limit(ENDPOINT, "app", requests=15, mins=15)
    @rate_limit(ENDPOINT, "user", requests=15, mins=15)
    def get(
        self,
        id: UserId,
        query: Optional[V2GetUserFollowersQueryParameters] = None,
    ) -> V2GetUserFollowersResponseBody:
        # flake8: noqa E501
        """
        ユーザのフォロワーの一覧を取得する。

        refer: https://developer.twitter.com/en/docs/twitter-api/users/follows/api-reference/get-users-id-followers
        """
        return self.request_client.get(
            endpoint=ENDPOINT,
            url=ENDPOINT.url.replace(":id", id),
            query=_make_query(query) if query is not None else None,
            response_type=V2GetUserFollowersResponseBody,
        )
