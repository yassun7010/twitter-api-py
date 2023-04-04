from datetime import datetime
from typing import Literal, NotRequired, Optional, TypedDict

from twitter_api.api.api_resources import ApiResources
from twitter_api.api.v2.types.expansion import Expansion
from twitter_api.api.v2.types.media.media_field import MediaField
from twitter_api.api.v2.types.place.place_field import PlaceField
from twitter_api.api.v2.types.poll.poll_field import PollField
from twitter_api.api.v2.types.tweet.tweet import Tweet
from twitter_api.api.v2.types.tweet.tweet_detail import TweetDetail
from twitter_api.api.v2.types.tweet.tweet_field import TweetField
from twitter_api.api.v2.types.tweet.tweet_id import TweetId
from twitter_api.api.v2.types.user.user_field import UserField
from twitter_api.api.v2.types.user.user_id import UserId
from twitter_api.rate_limit.rate_limit_decorator import rate_limit
from twitter_api.types.comma_separatable import CommaSeparatable, comma_separated_str
from twitter_api.types.endpoint import Endpoint
from twitter_api.types.extra_permissive_model import ExtraPermissiveModel
from twitter_api.utils.functional import map_optional

ENDPOINT = Endpoint("GET", "https://api.twitter.com/2/users/:id/tweets")

V2GetUserTweetsQueryParameters = TypedDict(
    "V2GetUserTweetsQueryParameters",
    {
        "start_time": NotRequired[Optional[datetime]],
        "end_time": NotRequired[Optional[datetime]],
        "since_id": NotRequired[Optional[TweetId]],
        "until_id": NotRequired[Optional[TweetId]],
        "exclude": NotRequired[Optional[Literal["retweets", "replies"]]],
        "expansions": NotRequired[Optional[CommaSeparatable[Expansion]]],
        "pagination_token": NotRequired[Optional[str]],
        "max_results": NotRequired[Optional[int]],
        "media.fields": NotRequired[Optional[CommaSeparatable[MediaField]]],
        "place.fields": NotRequired[Optional[CommaSeparatable[PlaceField]]],
        "poll.fields": NotRequired[Optional[CommaSeparatable[PollField]]],
        "tweet.fields": NotRequired[Optional[CommaSeparatable[TweetField]]],
        "user.fields": NotRequired[Optional[CommaSeparatable[UserField]]],
    },
)


def _make_query(query: V2GetUserTweetsQueryParameters) -> dict:
    return {
        "start_time": map_optional(lambda x: x.isoformat(), query.get("start_time")),
        "end_time": map_optional(lambda x: x.isoformat(), query.get("end_time")),
        "since_id": query.get("since_id"),
        "until_id": query.get("until_id"),
        "exclude": query.get("exclude"),
        "expansions": comma_separated_str(query.get("expansions")),
        "pagination_token": query.get("pagination_token"),
        "max_results": query.get("max_results"),
        "media.fields": comma_separated_str(query.get("media.fields")),
        "place.fields": comma_separated_str(query.get("place.fields")),
        "poll.fields": comma_separated_str(query.get("poll.fields")),
        "tweet.fields": comma_separated_str(query.get("tweet.fields")),
        "user.fields": comma_separated_str(query.get("user.fields")),
    }


class V2GetUserTweetsResponseBodyMeta(ExtraPermissiveModel):
    result_count: int
    oldest_id: TweetId
    newest_id: TweetId
    next_token: Optional[str] = None
    previous_token: Optional[str] = None


class V2GetUserTweetsResponseBodyIncludes(ExtraPermissiveModel):
    tweets: Optional[list[Tweet]] = None


class V2GetUserTweetsResponseBody(ExtraPermissiveModel):
    data: list[TweetDetail]
    meta: V2GetUserTweetsResponseBodyMeta
    includes: Optional[V2GetUserTweetsResponseBodyIncludes] = None


class V2GetUserTweetsResources(ApiResources):
    @rate_limit(ENDPOINT, "app", requests=1500, mins=15)
    @rate_limit(ENDPOINT, "user", requests=900, mins=15)
    def get(
        self,
        id: UserId,
        query: Optional[V2GetUserTweetsQueryParameters] = None,
    ) -> V2GetUserTweetsResponseBody:
        # flake8: noqa E501
        """
        ユーザのツイートの一覧を取得する。

        refer: https://developer.twitter.com/en/docs/twitter-api/tweets/timelines/api-reference/get-users-id-tweets
        """
        return self.request_client.get(
            endpoint=ENDPOINT,
            url=ENDPOINT.url.replace(":id", id),
            query=_make_query(query) if query is not None else None,
            response_type=V2GetUserTweetsResponseBody,
        )