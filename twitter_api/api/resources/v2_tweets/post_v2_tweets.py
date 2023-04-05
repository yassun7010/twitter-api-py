from typing import Literal, NotRequired, Optional, TypedDict

from twitter_api.api.resources.api_resources import ApiResources
from twitter_api.api.types.v2_media.media_id import MediaId
from twitter_api.api.types.v2_place.place_id import PlaceId
from twitter_api.api.types.v2_tweet.tweet_detail import TweetDetail
from twitter_api.api.types.v2_tweet.tweet_id import TweetId
from twitter_api.api.types.v2_user.user_id import UserId
from twitter_api.rate_limit.rate_limit_decorator import rate_limit
from twitter_api.types.endpoint import Endpoint
from twitter_api.types.extra_permissive_model import ExtraPermissiveModel
from twitter_api.types.http import Url, downcast_dict

ENDPOINT = Endpoint("POST", "https://api.twitter.com/2/tweets")


class V2PostTweetsGeospatialInformation(TypedDict):
    place_id: PlaceId
    tagged_user_ids: UserId


class V2PostTweetsMedia(TypedDict):
    media_ids: list[MediaId]
    tagged_user_ids: list[UserId]


class V2PostTweetsPoll(TypedDict):
    options: list[str]
    duration_minutes: int


class V2PostTweetsReply(TypedDict):
    exclude_reply_user_ids: list[UserId]
    in_reply_to_tweet_id: list[TweetId]


class V2PostTweetsRequestBody(TypedDict):
    direct_message_deep_link: NotRequired[Optional[Url]]
    for_super_followers_only: NotRequired[Optional[bool]]
    geo: NotRequired[Optional[V2PostTweetsGeospatialInformation]]
    media: NotRequired[Optional[V2PostTweetsMedia]]
    poll: NotRequired[Optional[V2PostTweetsPoll]]
    quote_tweet_id: NotRequired[Optional[TweetId]]
    reply: NotRequired[Optional[V2PostTweetsReply]]
    reply_settings: NotRequired[Optional[Literal["mentionedUsers", "following"]]]
    text: NotRequired[Optional[str]]


class V2PostTweetsResponseBody(ExtraPermissiveModel):
    data: TweetDetail


class V2PostTweetsResources(ApiResources):
    @rate_limit(ENDPOINT, "user", requests=200, mins=15)
    def post(self, request_body: V2PostTweetsRequestBody) -> V2PostTweetsResponseBody:
        # flake8: noqa E501
        """
        ツイートする。

        refer: https://developer.twitter.com/en/docs/twitter-api/tweets/manage-tweets/api-reference/post-tweets
        """
        return self.request_client.post(
            endpoint=ENDPOINT,
            response_type=V2PostTweetsResponseBody,
            json=downcast_dict(request_body),
        )
