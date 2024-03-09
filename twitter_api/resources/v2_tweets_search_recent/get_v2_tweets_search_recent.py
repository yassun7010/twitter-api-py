from datetime import datetime
from typing import Callable, Generator, Optional, Union

from typing_extensions import AsyncGenerator, Literal, NotRequired, TypedDict, override

from twitter_api.rate_limit.rate_limit import rate_limit
from twitter_api.resources.api_resources import ApiResources
from twitter_api.types._paging import (
    aget_paging_all,
    aget_paging_iter,
    get_paging_all,
    get_paging_iter,
)
from twitter_api.types.comma_separatable import CommaSeparatable, comma_separated_str
from twitter_api.types.endpoint import Endpoint
from twitter_api.types.pagination_token import PaginationToken
from twitter_api.types.v2_media.media_field import MediaField
from twitter_api.types.v2_place.place_field import PlaceField
from twitter_api.types.v2_poll.poll_field import PollField
from twitter_api.types.v2_scope import oauth2_scopes
from twitter_api.types.v2_search_query.operators.operator import CompleteOperator
from twitter_api.types.v2_search_query.search_query import SearchQuery
from twitter_api.types.v2_search_query.search_query_builder import SearchQueryBuilder
from twitter_api.types.v2_tweet.tweet_expansion import TweetExpansion
from twitter_api.types.v2_tweet.tweet_field import TweetField
from twitter_api.types.v2_tweet.tweet_id import TweetId
from twitter_api.types.v2_tweet.tweet_response_body import TweetsSearchResponseBody
from twitter_api.types.v2_user.user_field import UserField
from twitter_api.utils._datetime import rfc3339
from twitter_api.utils._functional import map_optional

ENDPOINT = Endpoint("GET", "https://api.twitter.com/2/tweets/search/recent")

GetV2TweetsSearchRecentQueryParameters = TypedDict(
    "GetV2TweetsSearchRecentQueryParameters",
    {
        "query": Union[
            str,
            SearchQuery,
            Callable[[SearchQueryBuilder], CompleteOperator],
        ],
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


def _make_query(query_params: GetV2TweetsSearchRecentQueryParameters) -> dict:
    query = (
        SearchQuery.build(query_params["query"])
        if callable(query_params["query"])
        else query_params["query"]
    )

    return {
        "query": str(query),
        "start_time": map_optional(rfc3339, query_params.get("start_time")),
        "end_time": map_optional(rfc3339, query_params.get("end_time")),
        "since_id": query_params.get("since_id"),
        "until_id": query_params.get("until_id"),
        "sort_order": query_params.get("sort_order"),
        "next_token": query_params.get("next_token"),
        "max_results": query_params.get("max_results"),
        "expansions": comma_separated_str(query_params.get("expansions")),
        "place.fields": comma_separated_str(query_params.get("place.fields")),
        "media.fields": comma_separated_str(query_params.get("media.fields")),
        "poll.fields": comma_separated_str(query_params.get("poll.fields")),
        "tweet.fields": comma_separated_str(query_params.get("tweet.fields")),
        "user.fields": comma_separated_str(query_params.get("user.fields")),
    }


class GetV2TweetsSearchRecentResponseBody(TweetsSearchResponseBody):
    pass


class GetV2TweetsSearchRecentResources(ApiResources):
    @oauth2_scopes(
        "tweet.read",
        "users.read",
    )
    @rate_limit(ENDPOINT, "app", requests=450, mins=15)
    @rate_limit(ENDPOINT, "user", requests=180, mins=15)
    def get(
        self, query: GetV2TweetsSearchRecentQueryParameters
    ) -> GetV2TweetsSearchRecentResponseBody:
        """
        ツイートの一覧を検索する。

        refer: https://developer.twitter.com/en/docs/twitter-api/tweets/search/api-reference/get-tweets-search-recent
        """
        return self.request_client.get(
            endpoint=ENDPOINT,
            response_body_type=GetV2TweetsSearchRecentResponseBody,
            query=_make_query(query) if query is not None else None,
        )

    def get_paging_iter(
        self, query: GetV2TweetsSearchRecentQueryParameters
    ) -> Generator[GetV2TweetsSearchRecentResponseBody, None, None]:
        """
        ツイートの一覧を検索する。

        ページングされた API のレスポンスをイテレータで返す。

        refer: https://developer.twitter.com/en/docs/twitter-api/tweets/search/api-reference/get-tweets-search-recent
        """
        return get_paging_iter(self.get, query, "next_token")

    def get_paging_all(
        self, query: GetV2TweetsSearchRecentQueryParameters
    ) -> GetV2TweetsSearchRecentResponseBody:
        """
        ツイートの一覧を検索する。

        ページングされた API のレスポンスをまとめて一つのレスポンスとして返す。

        refer: https://developer.twitter.com/en/docs/twitter-api/tweets/search/api-reference/get-tweets-search-recent
        """
        return get_paging_all(self.get, query, "next_token")


class AsyncGetV2TweetsSearchRecentResources(GetV2TweetsSearchRecentResources):
    @override
    async def get(
        self, query: GetV2TweetsSearchRecentQueryParameters
    ) -> GetV2TweetsSearchRecentResponseBody:
        return super().get(query)

    @override
    async def get_paging_iter(
        self, query: GetV2TweetsSearchRecentQueryParameters
    ) -> AsyncGenerator[GetV2TweetsSearchRecentResponseBody, None]:
        return aget_paging_iter(self.get, query, "next_token")

    @override
    async def get_paging_all(
        self, query: GetV2TweetsSearchRecentQueryParameters
    ) -> GetV2TweetsSearchRecentResponseBody:
        return await aget_paging_all(self.get, query, "next_token")
