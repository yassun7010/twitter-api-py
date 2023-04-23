from datetime import datetime
from typing import AsyncGenerator, Generator, NotRequired, Optional, TypedDict

from twitter_api.api.resources.api_resources import ApiResources
from twitter_api.api.types.v2_expansion import Expansion
from twitter_api.api.types.v2_media.media_field import MediaField
from twitter_api.api.types.v2_place.place_field import PlaceField
from twitter_api.api.types.v2_poll.poll_field import PollField
from twitter_api.api.types.v2_scope import oauth2_scopes
from twitter_api.api.types.v2_tweet.tweet_field import TweetField
from twitter_api.api.types.v2_tweet.tweet_response_body import TweetsSearchResponseBody
from twitter_api.api.types.v2_user.user_field import UserField
from twitter_api.rate_limit.rate_limit import rate_limit
from twitter_api.types.comma_separatable import CommaSeparatable, comma_separated_str
from twitter_api.types.endpoint import Endpoint
from twitter_api.types.paging import (
    get_collected_paging_response_async,
    get_collected_paging_response_sync,
    get_paging_response_iter_async,
    get_paging_response_iter_sync,
)
from twitter_api.utils.datetime import rfc3339
from twitter_api.utils.functional import map_optional

ENDPOINT = Endpoint("GET", "https://api.twitter.com/2/tweets/search/stream")

GetV2TweetsSearchStreamQueryParameters = TypedDict(
    "GetV2TweetsSearchStreamQueryParameters",
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
        return self.request_client.get(
            endpoint=ENDPOINT,
            response_type=GetV2TweetsSearchStreamResponseBody,
            query=_make_query(query) if query is not None else None,
        )

    def get_paging_response_iter(
        self, query: Optional[GetV2TweetsSearchStreamQueryParameters] = None
    ) -> Generator[GetV2TweetsSearchStreamResponseBody, None, None]:
        """
        ツイートの一覧を検索する。

        ページングされた API のレスポンスをイテレータで返す。

        refer: https://developer.twitter.com/en/docs/twitter-api/tweets/filtered-stream/api-reference/get-tweets-search-stream
        """
        return get_paging_response_iter_sync(self.get, query)

    def get_collected_response(
        self, query: Optional[GetV2TweetsSearchStreamQueryParameters] = None
    ) -> GetV2TweetsSearchStreamResponseBody:
        """
        ツイートの一覧を検索する。

        ページングされた API のレスポンスをまとめて一つのレスポンスとして返す。

        refer: https://developer.twitter.com/en/docs/twitter-api/tweets/filtered-stream/api-reference/get-tweets-search-stream
        """
        return get_collected_paging_response_sync(self.get, query)


class AsyncGetV2TweetsSearchStreamResources(GetV2TweetsSearchStreamResources):
    async def get(
        self, query: Optional[GetV2TweetsSearchStreamQueryParameters] = None
    ) -> GetV2TweetsSearchStreamResponseBody:
        return super().get(query)

    async def get_paging_response_iter(
        self, query: Optional[GetV2TweetsSearchStreamQueryParameters] = None
    ) -> AsyncGenerator[GetV2TweetsSearchStreamResponseBody, None]:
        return get_paging_response_iter_async(self.get, query)

    async def get_collected_response(
        self, query: Optional[GetV2TweetsSearchStreamQueryParameters] = None
    ) -> GetV2TweetsSearchStreamResponseBody:
        return await get_collected_paging_response_async(self.get, query)
