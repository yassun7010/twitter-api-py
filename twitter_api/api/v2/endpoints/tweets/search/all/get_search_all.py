from typing import Literal, NotRequired, Optional, TypeAlias, TypedDict

from twitter_api.api.v2.types.expansion import Expansion
from twitter_api.api.v2.types.retweet.retweet import Retweet
from twitter_api.api.v2.types.tweet.tweet_field import TweetField
from twitter_api.api.v2.types.tweet.tweet_id import TweetId
from twitter_api.api.v2.types.user.user import User
from twitter_api.api.v2.types.user.user_field import UserField
from twitter_api.client.request.request_client import RequestClient
from twitter_api.types.comma_separatable import CommaSeparatable, comma_separated_str
from twitter_api.types.endpoint import Endpoint
from twitter_api.types.extra_permissive_model import ExtraPermissiveModel
from twitter_api.utils.ratelimit import rate_limit

Uri: TypeAlias = Literal["https://api.twitter.com/2/tweets/search/all"]

ENDPOINT = Endpoint("GET", "https://api.twitter.com/2/tweets/search/all")

V2GetTweetsSearchAllQueryParameters = TypedDict(
    "V2GetTweetsSearchAllQueryParameters",
    {
        "expansions": NotRequired[Optional[CommaSeparatable[Expansion]]],
        "max_results": NotRequired[Optional[int]],
        "pagination_token": NotRequired[Optional[str]],
        "tweet.fields": NotRequired[Optional[CommaSeparatable[TweetField]]],
        "user.fields": NotRequired[Optional[CommaSeparatable[UserField]]],
    },
)


def _make_query(query: V2GetTweetsSearchAllQueryParameters) -> dict:
    return {
        "expansions": comma_separated_str(query.get("expansions")),
        "max_results": query.get("expansions"),
        "pagination_token": query.get("expansions"),
        "tweet.fields": comma_separated_str(query.get("tweet.fields")),
        "user.fields": comma_separated_str(query.get("user.fields")),
    }


class V2GetTweetsSearchAllResponseBodyMeta(ExtraPermissiveModel):
    result_count: int
    next_token: Optional[str] = None


class V2GetTweetsSearchAllResponseBody(ExtraPermissiveModel):
    data: list[Retweet]
    meta: V2GetTweetsSearchAllResponseBodyMeta


class V2GetTweetsSearchAll:
    def __init__(self, client: RequestClient) -> None:
        self._client = client

    @rate_limit("app", requests=300, mins=15)
    @rate_limit("user", requests=1, secs=1)
    def get(
        self, id: TweetId, query: Optional[V2GetTweetsSearchAllQueryParameters] = None
    ) -> V2GetTweetsSearchAllResponseBody:
        # flake8: noqa E501
        """
        リツイートされたツイートの一覧を取得する。

        refer: https://developer.twitter.com/en/docs/twitter-api/tweets/retweets/api-reference/get-tweets-id-retweeted_by
        """
        return self._client.get(
            endpoint=ENDPOINT,
            response_type=V2GetTweetsSearchAllResponseBody,
            url=ENDPOINT.url.replace(":id", id),
            query=_make_query(query) if query is not None else None,
        )
