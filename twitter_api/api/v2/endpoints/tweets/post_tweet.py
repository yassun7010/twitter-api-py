from typing import Literal, NotRequired, Optional, TypedDict

from twitter_api.api.v2.types.media.media_id import MediaId
from twitter_api.api.v2.types.place.place_id import PlaceId
from twitter_api.api.v2.types.tweet.tweet import Tweet
from twitter_api.api.v2.types.tweet.tweet_id import TweetId
from twitter_api.api.v2.types.user.user import User
from twitter_api.api.v2.types.user.user_id import UserId
from twitter_api.client.request.request_client import RequestClient
from twitter_api.types.endpoint import Endpoint
from twitter_api.types.extra_permissive_model import ExtraPermissiveModel
from twitter_api.types.http import Url, downcast_dict
from twitter_api.utils.ratelimit import rate_limit

ENDPOINT = Endpoint("POST", "https://api.twitter.com/2/tweets")


class V2PostTweetGeospatialInformation(TypedDict):
    place_id: PlaceId
    tagged_user_ids: UserId


class V2PostTweetMedia(TypedDict):
    media_ids: list[MediaId]
    tagged_user_ids: list[UserId]


class V2PostTweetPoll(TypedDict):
    options: list[str]
    duration_minutes: int


class V2PostTweetReply(TypedDict):
    exclude_reply_user_ids: list[UserId]
    in_reply_to_tweet_id: list[TweetId]


class V2PostTweetRequestBody(TypedDict):
    direct_message_deep_link: NotRequired[Optional[Url]]
    for_super_followers_only: NotRequired[Optional[bool]]
    geo: NotRequired[Optional[V2PostTweetGeospatialInformation]]
    media: NotRequired[Optional[V2PostTweetMedia]]
    poll: NotRequired[Optional[V2PostTweetPoll]]
    quote_tweet_id: NotRequired[Optional[TweetId]]
    reply: NotRequired[Optional[V2PostTweetReply]]
    reply_settings: NotRequired[Optional[Literal["mentionedUsers", "following"]]]
    text: NotRequired[Optional[str]]


class V2PostTweetResponseBody(ExtraPermissiveModel):
    data: Tweet


class V2PostTweet:
    def __init__(self, client: RequestClient) -> None:
        self._client = client

    @rate_limit("user", requests=200, mins=15)
    def post(self, request_body: V2PostTweetRequestBody) -> V2PostTweetResponseBody:
        # flake8: noqa E501
        """
        ツイートする。

        refer: https://developer.twitter.com/en/docs/twitter-api/tweets/manage-tweets/api-reference/post-tweets
        """
        return self._client.post(
            endpoint=ENDPOINT,
            response_type=V2PostTweetResponseBody,
            json=downcast_dict(request_body),
        )
