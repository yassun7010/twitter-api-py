from datetime import datetime
from typing import (
    AsyncGenerator,
    Generator,
    Literal,
    NotRequired,
    Optional,
    TypedDict,
    Union,
)
from urllib import parse

from twitter_api.rate_limit.rate_limit import rate_limit
from twitter_api.resources.api_resources import ApiResources
from twitter_api.types._paging import (
    get_collected_paging_response_body_async,
    get_collected_paging_response_body_sync,
    get_paging_response_body_iter_async,
    get_paging_response_body_iter_sync,
)
from twitter_api.types.comma_separatable import CommaSeparatable, comma_separated_str
from twitter_api.types.endpoint import Endpoint
from twitter_api.types.pagination_token import PaginationToken
from twitter_api.types.v2_media.media_field import MediaField
from twitter_api.types.v2_place.place_field import PlaceField
from twitter_api.types.v2_poll.poll_field import PollField
from twitter_api.types.v2_scope import oauth2_scopes
from twitter_api.types.v2_search_query.search_query import SearchQuery
from twitter_api.types.v2_tweet.tweet_expansion import TweetExpansion
from twitter_api.types.v2_tweet.tweet_field import TweetField
from twitter_api.types.v2_tweet.tweet_id import TweetId
from twitter_api.types.v2_tweet.tweet_response_body import TweetsSearchResponseBody
from twitter_api.types.v2_user.user_field import UserField
from twitter_api.utils._datetime import rfc3339
from twitter_api.utils._functional import map_optional

ENDPOINT = Endpoint("GET", "https://api.twitter.com/2/tweets/search/all")

GetV2TweetsSearchAllQueryParameters = TypedDict(
    "GetV2TweetsSearchAllQueryParameters",
    {
        "query": Union[SearchQuery, str],
        "start_time": NotRequired[Optional[datetime]],
        "end_time": NotRequired[Optional[datetime]],
        "since_id": NotRequired[Optional[TweetId]],
        "until_id": NotRequired[Optional[TweetId]],
        "sort_order": NotRequired[Optional[Literal["recency", "relevancy"]]],
        "next_token": NotRequired[Optional[PaginationToken]],
        "max_results": NotRequired[Optional[int]],
        "expansions": NotRequired[Optional[CommaSeparatable[TweetExpansion]]],
        "place.fields": NotRequired[Optional[CommaSeparatable[PlaceField]]],
        "media.fields": NotRequired[Optional[CommaSeparatable[MediaField]]],
        "poll.fields": NotRequired[Optional[CommaSeparatable[PollField]]],
        "tweet.fields": NotRequired[Optional[CommaSeparatable[TweetField]]],
        "user.fields": NotRequired[Optional[CommaSeparatable[UserField]]],
    },
)


def _make_query(query: GetV2TweetsSearchAllQueryParameters) -> dict:
    return {
        "query": parse.quote(str(query["query"])),
        "start_time": map_optional(rfc3339, query.get("start_time")),
        "end_time": map_optional(rfc3339, query.get("end_time")),
        "since_id": query.get("since_id"),
        "until_id": query.get("until_id"),
        "sort_order": query.get("sort_order"),
        "next_token": query.get("next_token"),
        "max_results": query.get("expansions"),
        "expansions": comma_separated_str(query.get("expansions")),
        "place.fields": query.get("place.fields"),
        "media.fields": query.get("media.fields"),
        "poll.fields": query.get("poll.fields"),
        "tweet.fields": comma_separated_str(query.get("tweet.fields")),
        "user.fields": comma_separated_str(query.get("user.fields")),
    }


class GetV2TweetsSearchAllResponseBody(TweetsSearchResponseBody):
    pass


class GetV2TweetsSearchAllResources(ApiResources):
    @oauth2_scopes(
        "tweet.read",
        "users.read",
    )
    @rate_limit(ENDPOINT, "app", requests=300, mins=15)
    @rate_limit(ENDPOINT, "app", requests=1, seconds=1)
    def get(
        self, query: GetV2TweetsSearchAllQueryParameters
    ) -> GetV2TweetsSearchAllResponseBody:
        """
        ツイートの一覧を検索する。

        refer: https://developer.twitter.com/en/docs/twitter-api/tweets/search/api-reference/get-tweets-search-all
        """
        return self.request_client.get(
            endpoint=ENDPOINT,
            response_body_type=GetV2TweetsSearchAllResponseBody,
            query=_make_query(query) if query is not None else None,
        )

    def get_paging_response_body_iter(
        self, query: GetV2TweetsSearchAllQueryParameters
    ) -> Generator[GetV2TweetsSearchAllResponseBody, None, None]:
        """
        ツイートの一覧を検索する。

        ページングされた API のレスポンスをイテレータで返す。

        refer: https://developer.twitter.com/en/docs/twitter-api/tweets/search/api-reference/get-tweets-search-all
        """
        return get_paging_response_body_iter_sync(self.get, query, "next_token")

    def get_collected_paging_response_body(
        self, query: GetV2TweetsSearchAllQueryParameters
    ) -> GetV2TweetsSearchAllResponseBody:
        """
        ツイートの一覧を検索する。

        ページングされた API のレスポンスをまとめて一つのレスポンスとして返す。

        refer: https://developer.twitter.com/en/docs/twitter-api/tweets/search/api-reference/get-tweets-search-all
        """
        return get_collected_paging_response_body_sync(self.get, query, "next_token")


class AsyncGetV2TweetsSearchAllResources(GetV2TweetsSearchAllResources):
    async def get(
        self, query: GetV2TweetsSearchAllQueryParameters
    ) -> GetV2TweetsSearchAllResponseBody:
        return super().get(query)

    async def get_paging_response_body_iter(
        self, query: GetV2TweetsSearchAllQueryParameters
    ) -> AsyncGenerator[GetV2TweetsSearchAllResponseBody, None]:
        return get_paging_response_body_iter_async(self.get, query, "next_token")

    async def get_collected_paging_response_body(
        self, query: GetV2TweetsSearchAllQueryParameters
    ) -> GetV2TweetsSearchAllResponseBody:
        return await get_collected_paging_response_body_async(
            self.get, query, "next_token"
        )
