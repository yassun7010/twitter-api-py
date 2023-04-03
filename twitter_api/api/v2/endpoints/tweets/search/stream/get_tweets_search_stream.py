from datetime import datetime
from typing import NotRequired, Optional, TypedDict

from twitter_api.api.v2.types.expansion import Expansion
from twitter_api.api.v2.types.media.media_field import MediaField
from twitter_api.api.v2.types.place.place_field import PlaceField
from twitter_api.api.v2.types.poll.poll_field import PollField
from twitter_api.api.v2.types.tweet.tweet_detail import TweetDetail
from twitter_api.api.v2.types.tweet.tweet_field import TweetField
from twitter_api.api.v2.types.user.user_field import UserField
from twitter_api.client.types.api_resources import ApiResources
from twitter_api.rate_limit.rate_limit_decorator import rate_limit
from twitter_api.types.comma_separatable import CommaSeparatable, comma_separated_str
from twitter_api.types.endpoint import Endpoint
from twitter_api.types.extra_permissive_model import ExtraPermissiveModel
from twitter_api.utils.functional import map_optional

ENDPOINT = Endpoint("GET", "https://api.twitter.com/2/tweets/search/stream")

V2GetTweetsSearchStreamQueryParameters = TypedDict(
    "V2GetTweetsSearchStreamQueryParameters",
    {
        "backfill_minutes": NotRequired[Optional[int]],
        "start_time": NotRequired[Optional[datetime]],
        "end_time": NotRequired[Optional[datetime]],
        "expansions": NotRequired[Optional[CommaSeparatable[Expansion]]],
        "place.fields": NotRequired[Optional[CommaSeparatable[PlaceField]]],
        "media.fields": NotRequired[Optional[CommaSeparatable[MediaField]]],
        "poll.fields": NotRequired[Optional[CommaSeparatable[PollField]]],
        "tweet.fields": NotRequired[Optional[CommaSeparatable[TweetField]]],
        "user.fields": NotRequired[Optional[CommaSeparatable[UserField]]],
    },
)


def _make_query(query: V2GetTweetsSearchStreamQueryParameters) -> dict:
    return {
        "backfill_minutes": query.get("backfill_minutes"),
        "start_time": map_optional(lambda x: x.isoformat(), query.get("start_time")),
        "end_time": map_optional(lambda x: x.isoformat(), query.get("end_time")),
        "expansions": comma_separated_str(query.get("expansions")),
        "place.fields": query.get("place.fields"),
        "media.fields": query.get("media.fields"),
        "poll.fields": query.get("poll.fields"),
        "tweet.fields": comma_separated_str(query.get("tweet.fields")),
        "user.fields": comma_separated_str(query.get("user.fields")),
    }


class V2GetTweetsSearchStreamResponseBody(ExtraPermissiveModel):
    data: Optional[list[TweetDetail]] = None  # データが 1 つも見つからないとき、 None となる。


class V2GetTweetsSearchStreamResources(ApiResources):
    @rate_limit(ENDPOINT, "app", requests=50, mins=15)
    def get(
        self, query: Optional[V2GetTweetsSearchStreamQueryParameters] = None
    ) -> V2GetTweetsSearchStreamResponseBody:
        # flake8: noqa E501
        """
        ツイートの一覧を検索する。

        refer: https://developer.twitter.com/en/docs/twitter-api/tweets/filtered-stream/api-reference/get-tweets-search-stream
        """
        return self._client.get(
            endpoint=ENDPOINT,
            response_type=V2GetTweetsSearchStreamResponseBody,
            query=_make_query(query) if query is not None else None,
        )
