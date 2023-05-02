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
from twitter_api.types.v2_tweet.tweet_id import TweetId
from twitter_api.types.v2_tweet.tweet_response_body import TweetResponseBody
from twitter_api.types.v2_user.user_field import UserField

ENDPOINT = Endpoint("GET", "https://api.twitter.com/2/tweets/:id")

GetV2TweetQueryParameters = TypedDict(
    "GetV2TweetQueryParameters",
    {
        "expansions": NotRequired[Optional[CommaSeparatable[TweetExpansion]]],
        "media.fields": NotRequired[Optional[CommaSeparatable[MediaField]]],
        "place.fields": NotRequired[Optional[CommaSeparatable[PlaceField]]],
        "poll.fields": NotRequired[Optional[CommaSeparatable[PollField]]],
        "tweet.fields": NotRequired[Optional[CommaSeparatable[TweetField]]],
        "user.fields": NotRequired[Optional[CommaSeparatable[UserField]]],
    },
)


def _make_query(
    query: Optional[GetV2TweetQueryParameters],
) -> Optional[dict]:
    if query is None:
        return None

    return {
        "expansions": comma_separated_str(query.get("expansions")),
        "media.fields": comma_separated_str(query.get("media.fields")),
        "place.fields": comma_separated_str(query.get("place.fields")),
        "poll.fields": comma_separated_str(query.get("poll.fields")),
        "tweet.fields": comma_separated_str(query.get("tweet.fields")),
        "user.fields": comma_separated_str(query.get("user.fields")),
    }


class GetV2TweetResponseBody(TweetResponseBody):
    pass


class GetV2TweetResources(ApiResources):
    @oauth2_scopes(
        "tweet.read",
        "users.read",
    )
    @rate_limit(ENDPOINT, "app", requests=300, mins=15)
    @rate_limit(ENDPOINT, "user", requests=900, mins=15)
    def get(
        self,
        id: TweetId,
        query: Optional[GetV2TweetQueryParameters] = None,
    ) -> GetV2TweetResponseBody:
        """
        ツイートを取得する。

        refer: https://developer.twitter.com/en/docs/twitter-api/tweets/lookup/api-reference/get-tweets-id
        """
        return self.request_client.get(
            endpoint=ENDPOINT,
            response_body_type=GetV2TweetResponseBody,
            url=ENDPOINT.url.replace(":id", id),
            query=_make_query(query),
        )


class AsyncGetV2TweetResources(GetV2TweetResources):
    async def get(
        self,
        id: TweetId,
        query: Optional[GetV2TweetQueryParameters] = None,
    ):
        return super().get(id, query)
