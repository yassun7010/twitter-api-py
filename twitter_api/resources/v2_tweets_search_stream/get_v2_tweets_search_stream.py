from datetime import datetime
from typing import NotRequired, Optional, TypedDict

from twitter_api.rate_limit.rate_limit import rate_limit
from twitter_api.resources.api_resources import ApiResources
from twitter_api.types.comma_separatable import CommaSeparatable, comma_separated_str
from twitter_api.types.endpoint import Endpoint
from twitter_api.types.v2_media.media_field import MediaField
from twitter_api.types.v2_place.place_field import PlaceField
from twitter_api.types.v2_poll.poll_field import PollField
from twitter_api.types.v2_scope import oauth2_scopes
from twitter_api.types.v2_tweet.tweet_expansion import TweetExpansion
from twitter_api.types.v2_tweet.tweet_field import TweetField
from twitter_api.types.v2_tweet.tweet_response_body import TweetsSearchResponseBody
from twitter_api.types.v2_user.user_field import UserField
from twitter_api.utils._datetime import rfc3339
from twitter_api.utils._functional import map_optional

ENDPOINT = Endpoint("GET", "https://api.twitter.com/2/tweets/search/stream")

GetV2TweetsSearchStreamQueryParameters = TypedDict(
    "GetV2TweetsSearchStreamQueryParameters",
    {
        "backfill_minutes": NotRequired[Optional[int]],
        "start_time": NotRequired[Optional[datetime]],
        "end_time": NotRequired[Optional[datetime]],
        "expansions": NotRequired[Optional[CommaSeparatable[TweetExpansion]]],
        "place.fields": NotRequired[Optional[CommaSeparatable[PlaceField]]],
        "media.fields": NotRequired[Optional[CommaSeparatable[MediaField]]],
        "poll.fields": NotRequired[Optional[CommaSeparatable[PollField]]],
        "tweet.fields": NotRequired[Optional[CommaSeparatable[TweetField]]],
        "user.fields": NotRequired[Optional[CommaSeparatable[UserField]]],
    },
)


def _make_query(query: GetV2TweetsSearchStreamQueryParameters) -> dict:
    return {
        "backfill_minutes": query.get("backfill_minutes"),
        "start_time": map_optional(rfc3339, query.get("start_time")),
        "end_time": map_optional(rfc3339, query.get("end_time")),
        "expansions": comma_separated_str(query.get("expansions")),
        "place.fields": query.get("place.fields"),
        "media.fields": query.get("media.fields"),
        "poll.fields": query.get("poll.fields"),
        "tweet.fields": comma_separated_str(query.get("tweet.fields")),
        "user.fields": comma_separated_str(query.get("user.fields")),
    }


class GetV2TweetsSearchStreamResponseBody(TweetsSearchResponseBody):
    pass


class GetV2TweetsSearchStreamResources(ApiResources):
    @oauth2_scopes(
        "tweet.read",
        "users.read",
    )
    @rate_limit(ENDPOINT, "app", requests=50, mins=15)
    def get(
        self, query: Optional[GetV2TweetsSearchStreamQueryParameters] = None
    ) -> GetV2TweetsSearchStreamResponseBody:
        """
        ツイートの一覧を検索する。

        refer: https://developer.twitter.com/en/docs/twitter-api/tweets/filtered-stream/api-reference/get-tweets-search-stream
        """
        # TODO: stream で実装する必要があるが、開発用アカウントが凍結されたので検証できない。
        return self.request_client.get(
            endpoint=ENDPOINT,
            response_body_type=GetV2TweetsSearchStreamResponseBody,
            query=_make_query(query) if query is not None else None,
        )


class AsyncGetV2TweetsSearchStreamResources(GetV2TweetsSearchStreamResources):
    async def get(
        self, query: Optional[GetV2TweetsSearchStreamQueryParameters] = None
    ) -> GetV2TweetsSearchStreamResponseBody:
        return super().get(query)
