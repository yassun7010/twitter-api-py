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
from twitter_api.ratelimit.ratelimit_decorator import rate_limit
from twitter_api.types.comma_separatable import CommaSeparatable, comma_separated_str
from twitter_api.types.endpoint import Endpoint
from twitter_api.types.extra_permissive_model import ExtraPermissiveModel

ENDPOINT = Endpoint("DELETE", "https://api.twitter.com/2/tweets/:id")


class V2DeleteTweetResponseBodyData(ExtraPermissiveModel):
    deleted: bool


class V2DeleteTweetResponseBody(ExtraPermissiveModel):
    data: V2DeleteTweetResponseBodyData


class V2DeleteTweet:
    def __init__(self, client: RequestClient) -> None:
        self._client = client

    @rate_limit("user", requests=50, mins=15)
    def delete(
        self,
        id: TweetId,
    ) -> V2DeleteTweetResponseBody:
        # flake8: noqa E501
        """
        ツイートを削除する。

        refer: https://developer.twitter.com/en/docs/twitter-api/tweets/manage-tweets/api-reference/delete-tweets-id
        """
        return self._client.delete(
            endpoint=ENDPOINT,
            response_type=V2DeleteTweetResponseBody,
            url=ENDPOINT.url.replace(":id", id),
        )
