from typing import NotRequired, Optional, TypedDict

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
from twitter_api.ratelimit.manager.ratelimit_manager import RatelimitManager
from twitter_api.ratelimit.ratelimit_decorator import rate_limit
from twitter_api.ratelimit.ratelimit_interface import RatelimitInterface
from twitter_api.types.comma_separatable import CommaSeparatable, comma_separated_str
from twitter_api.types.endpoint import Endpoint
from twitter_api.types.extra_permissive_model import ExtraPermissiveModel

ENDPOINT = Endpoint("GET", "https://api.twitter.com/2/tweets/:id")

V2GetTweetQueryParameters = TypedDict(
    "V2GetTweetQueryParameters",
    {
        "expansions": NotRequired[Optional[CommaSeparatable[Expansion]]],
        "media.fields": NotRequired[Optional[CommaSeparatable[MediaField]]],
        "place.fields": NotRequired[Optional[CommaSeparatable[PlaceField]]],
        "poll.fields": NotRequired[Optional[CommaSeparatable[PollField]]],
        "tweet.fields": NotRequired[Optional[CommaSeparatable[TweetField]]],
        "user.fields": NotRequired[Optional[CommaSeparatable[UserField]]],
    },
)


def _make_query(
    query_parameters: Optional[V2GetTweetQueryParameters],
) -> Optional[dict]:
    if query_parameters is None:
        return None

    return {
        "expansions": comma_separated_str(query_parameters.get("expansions")),
        "media.fields": comma_separated_str(query_parameters.get("media.fields")),
        "place.fields": comma_separated_str(query_parameters.get("place.fields")),
        "poll.fields": comma_separated_str(query_parameters.get("poll.fields")),
        "tweet.fields": comma_separated_str(query_parameters.get("tweet.fields")),
        "user.fields": comma_separated_str(query_parameters.get("user.fields")),
    }


class V2GetTweetResponseBodyIncludes(ExtraPermissiveModel):
    users: list[User]


class V2GetTweetResponseBody(ExtraPermissiveModel):
    data: Tweet
    includes: Optional[V2GetTweetResponseBodyIncludes] = None


class V2GetTweet(RatelimitInterface):
    def __init__(self, client: RequestClient, ratelimit: RatelimitManager) -> None:
        self._client = client
        self._ratelimit = ratelimit

    @property
    def ratelimit(self) -> RatelimitManager:
        return self._ratelimit

    @rate_limit(ENDPOINT, "app", requests=300, mins=15)
    @rate_limit(ENDPOINT, "user", requests=900, mins=15)
    def get(
        self,
        id: TweetId,
        query: Optional[V2GetTweetQueryParameters] = None,
    ) -> V2GetTweetResponseBody:
        # flake8: noqa E501
        """
        ツイートの一覧を取得する。

        refer: https://developer.twitter.com/en/docs/twitter-api/tweets/lookup/api-reference/get-tweets
        """
        return self._client.get(
            endpoint=ENDPOINT,
            response_type=V2GetTweetResponseBody,
            url=ENDPOINT.url.replace(":id", id),
            query=_make_query(query),
        )
