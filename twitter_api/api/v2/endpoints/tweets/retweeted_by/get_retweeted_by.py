from typing import Literal, NotRequired, Optional, TypeAlias, TypedDict

from twitter_api.api.v2.types.expansion import Expansion
from twitter_api.api.v2.types.retweet.retweet import Retweet
from twitter_api.api.v2.types.tweet.tweet_field import TweetField
from twitter_api.api.v2.types.tweet.tweet_id import TweetId
from twitter_api.api.v2.types.user.user import User
from twitter_api.api.v2.types.user.user_field import UserField
from twitter_api.client.request.has_request_client import HasReqeustClient
from twitter_api.client.request.request_client import RequestClient
from twitter_api.rate_limit.manager.rate_limit_manager import RateLimitManager
from twitter_api.rate_limit.rate_limit_decorator import rate_limit
from twitter_api.types.comma_separatable import CommaSeparatable, comma_separated_str
from twitter_api.types.endpoint import Endpoint
from twitter_api.types.extra_permissive_model import ExtraPermissiveModel

Uri: TypeAlias = Literal["https://api.twitter.com/2/tweets/:id/retweeted_by"]

ENDPOINT = Endpoint("GET", "https://api.twitter.com/2/tweets/:id/retweeted_by")

V2GetRetweetedByQueryParameters = TypedDict(
    "V2GetRetweetedByQueryParameters",
    {
        "expansions": NotRequired[Optional[CommaSeparatable[Expansion]]],
        "max_results": NotRequired[Optional[int]],
        "pagination_token": NotRequired[Optional[str]],
        "tweet.fields": NotRequired[Optional[CommaSeparatable[TweetField]]],
        "user.fields": NotRequired[Optional[CommaSeparatable[UserField]]],
    },
)


def _make_query(query: V2GetRetweetedByQueryParameters) -> dict:
    return {
        "expansions": comma_separated_str(query.get("expansions")),
        "max_results": query.get("expansions"),
        "pagination_token": query.get("expansions"),
        "tweet.fields": comma_separated_str(query.get("tweet.fields")),
        "user.fields": comma_separated_str(query.get("user.fields")),
    }


class V2GetRetweetedByResponseBodyMeta(ExtraPermissiveModel):
    result_count: int
    next_token: Optional[str] = None


class V2GetRetweetedByResponseBody(ExtraPermissiveModel):
    data: list[Retweet]
    meta: V2GetRetweetedByResponseBodyMeta


class V2GetRetweetedBy(HasReqeustClient):
    def __init__(self, client: RequestClient) -> None:
        self._client = client

    @property
    def request_client(self) -> RequestClient:
        return self._client

    @rate_limit(ENDPOINT, "app", requests=75, mins=15)
    @rate_limit(ENDPOINT, "user", requests=75, mins=15)
    def get(
        self, id: TweetId, query: Optional[V2GetRetweetedByQueryParameters] = None
    ) -> V2GetRetweetedByResponseBody:
        # flake8: noqa E501
        """
        リツイートされたツイートの一覧を取得する。

        refer: https://developer.twitter.com/en/docs/twitter-api/tweets/retweets/api-reference/get-tweets-id-retweeted_by
        """
        return self._client.get(
            endpoint=ENDPOINT,
            response_type=V2GetRetweetedByResponseBody,
            url=ENDPOINT.url.replace(":id", id),
            query=_make_query(query) if query is not None else None,
        )
