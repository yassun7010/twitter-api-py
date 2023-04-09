from typing import NotRequired, Optional, TypedDict

from twitter_api.api.resources.api_resources import ApiResources
from twitter_api.api.types.v2_expansion import Expansion
from twitter_api.api.types.v2_media.media_field import MediaField
from twitter_api.api.types.v2_place.place_field import PlaceField
from twitter_api.api.types.v2_poll.poll_field import PollField
from twitter_api.api.types.v2_scope import oauth2_scopes
from twitter_api.api.types.v2_tweet.tweet import Tweet
from twitter_api.api.types.v2_tweet.tweet_detail import TweetDetail
from twitter_api.api.types.v2_tweet.tweet_field import TweetField
from twitter_api.api.types.v2_user.user_field import UserField
from twitter_api.api.types.v2_user.user_id import UserId
from twitter_api.rate_limit.rate_limit_decorator import rate_limit
from twitter_api.types.comma_separatable import CommaSeparatable, comma_separated_str
from twitter_api.types.endpoint import Endpoint
from twitter_api.types.extra_permissive_model import ExtraPermissiveModel

ENDPOINT = Endpoint("GET", "https://api.twitter.com/2/users/:id/liked_tweets")

GetV2UserLikedTweetsQueryParameters = TypedDict(
    "GetV2UserLikedTweetsQueryParameters",
    {
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


def _make_query(query: GetV2UserLikedTweetsQueryParameters) -> dict:
    return {
        "expansions": comma_separated_str(query.get("expansions")),
        "pagination_token": query.get("pagination_token"),
        "max_results": query.get("max_results"),
        "media.fields": comma_separated_str(query.get("media.fields")),
        "place.fields": comma_separated_str(query.get("place.fields")),
        "poll.fields": comma_separated_str(query.get("poll.fields")),
        "tweet.fields": comma_separated_str(query.get("tweet.fields")),
        "user.fields": comma_separated_str(query.get("user.fields")),
    }


class GetV2UserLikedTweetsResponseBodyIncludes(ExtraPermissiveModel):
    tweets: list[Tweet]


class GetV2UserLikedTweetsResponseBodyMeta(ExtraPermissiveModel):
    next_token: Optional[str] = None
    result_count: int


class GetV2UserLikedTweetsResponseBody(ExtraPermissiveModel):
    data: list[TweetDetail]
    includes: Optional[GetV2UserLikedTweetsResponseBodyIncludes] = None
    meta: Optional[GetV2UserLikedTweetsResponseBodyMeta] = None


class GetV2UserLikedTweetsResources(ApiResources):
    @oauth2_scopes(
        "tweet.read",
        "users.read",
        "like.read",
    )
    @rate_limit(ENDPOINT, "app", requests=75, mins=15)
    @rate_limit(ENDPOINT, "user", requests=75, mins=15)
    def get(
        self,
        id: UserId,
        query: Optional[GetV2UserLikedTweetsQueryParameters] = None,
    ) -> GetV2UserLikedTweetsResponseBody:
        # flake8: noqa E501
        """
        ユーザが「いいね」をしているツイートの一覧を取得する。

        refer: https://developer.twitter.com/en/docs/twitter-api/tweets/likes/api-reference/get-users-id-liked_tweets
        """
        return self.request_client.get(
            endpoint=ENDPOINT,
            url=ENDPOINT.url.replace(":id", id),
            query=_make_query(query) if query is not None else None,
            response_type=GetV2UserLikedTweetsResponseBody,
        )
