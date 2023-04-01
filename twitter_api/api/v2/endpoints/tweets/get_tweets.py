from typing import Literal, NotRequired, Optional, TypedDict

from twitter_api.api.v2.types.expansion import Expansion
from twitter_api.api.v2.types.media.media_field import MediaField
from twitter_api.api.v2.types.place.place_field import PlaceField
from twitter_api.api.v2.types.poll.poll_field import PollField
from twitter_api.api.v2.types.tweet.tweet import Tweet
from twitter_api.api.v2.types.tweet.tweet_field import TweetField
from twitter_api.api.v2.types.tweet.tweet_id import TweetId
from twitter_api.api.v2.types.user.user import User
from twitter_api.api.v2.types.user.user_field import UserField
from twitter_api.client.request.request_client import RequestClient
from twitter_api.types.comma_separatable import CommaSeparatable, comma_separated_str
from twitter_api.types.endpoint import Endpoint
from twitter_api.types.extra_permissive_model import ExtraPermissiveModel
from twitter_api.utils.ratelimit import rate_limit

ENDPOINT = Endpoint("GET", "/2/tweets")

V2GetTweetsQueryParameters = TypedDict(
    "V2GetTweetsQueryParameters",
    {
        "ids": CommaSeparatable[TweetId],
        "expansions": NotRequired[Optional[CommaSeparatable[Expansion]]],
        "media.fields": NotRequired[Optional[CommaSeparatable[MediaField]]],
        "place.fields": NotRequired[Optional[CommaSeparatable[PlaceField]]],
        "poll.fields": NotRequired[Optional[CommaSeparatable[PollField]]],
        "tweet.fields": NotRequired[Optional[CommaSeparatable[TweetField]]],
        "user.fields": NotRequired[Optional[CommaSeparatable[UserField]]],
    },
)


def _make_query(query: V2GetTweetsQueryParameters) -> dict:
    return {
        "ids": comma_separated_str(query["ids"]),
        "expansions": comma_separated_str(query.get("expansions")),
        "media.fields": comma_separated_str(query.get("media.fields")),
        "place.fields": comma_separated_str(query.get("place.fields")),
        "poll.fields": comma_separated_str(query.get("poll.fields")),
        "tweet.fields": comma_separated_str(query.get("tweet.fields")),
        "user.fields": comma_separated_str(query.get("user.fields")),
    }


class V2GetTweetsResponseBodyIncludes(ExtraPermissiveModel):
    users: list[User]


class V2GetTweetsResponseBody(ExtraPermissiveModel):
    data: list[Tweet]
    includes: Optional[V2GetTweetsResponseBodyIncludes] = None


class V2GetTweets:
    def __init__(self, client: RequestClient) -> None:
        self._client = client

    @rate_limit(per="app", requests=300, mins=15)
    @rate_limit(per="user", requests=900, mins=15)
    def get(self, query: V2GetTweetsQueryParameters) -> V2GetTweetsResponseBody:
        # flake8: noqa E501
        """
        ツイートの一覧を取得する。

        refer: https://developer.twitter.com/en/docs/twitter-api/tweets/lookup/api-reference/get-tweets
        """
        return self._client.get(
            endpoint=ENDPOINT,
            query=_make_query(query),
            response_type=V2GetTweetsResponseBody,
        )
