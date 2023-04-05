from typing import Literal, NotRequired, Optional, TypedDict, Union

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


class PostV2TweetsGeospatialInformation(TypedDict):
    place_id: PlaceId
    tagged_user_ids: UserId


class PostV2TweetsMedia(TypedDict):
    media_ids: list[MediaId]
    tagged_user_ids: NotRequired[list[UserId]]


class PostV2TweetsPoll(TypedDict):
    options: list[str]
    duration_minutes: int


class PostV2TweetsReply(TypedDict):
    exclude_reply_user_ids: list[UserId]
    in_reply_to_tweet_id: list[TweetId]


class _PostV2TweetsRequestBodyBase(TypedDict):
    direct_message_deep_link: NotRequired[Optional[Url]]
    for_super_followers_only: NotRequired[Optional[bool]]
    geo: NotRequired[Optional[PostV2TweetsGeospatialInformation]]
    poll: NotRequired[Optional[PostV2TweetsPoll]]
    quote_tweet_id: NotRequired[Optional[TweetId]]
    reply: NotRequired[Optional[PostV2TweetsReply]]
    reply_settings: NotRequired[Optional[Literal["mentionedUsers", "following"]]]


class PostV2TweetsRequestBodyMedia(_PostV2TweetsRequestBodyBase):
    text: NotRequired[Optional[str]]
    media: PostV2TweetsMedia


class PostV2TweetsRequestBodyText(_PostV2TweetsRequestBodyBase):
    text: str
    media: NotRequired[Optional[PostV2TweetsMedia]]


PostV2TweetsRequestBody = Union[
    PostV2TweetsRequestBodyText,
    PostV2TweetsRequestBodyMedia,
]


class PostV2TweetsResponseBody(ExtraPermissiveModel):
    data: TweetDetail


class PostV2TweetsResources(ApiResources):
    @rate_limit(ENDPOINT, "user", requests=200, mins=15)
    def post(self, request_body: PostV2TweetsRequestBody) -> PostV2TweetsResponseBody:
        # flake8: noqa E501
        """
        ツイートする。

        refer: https://developer.twitter.com/en/docs/twitter-api/tweets/manage-tweets/api-reference/post-tweets
        """
        return self.request_client.post(
            endpoint=ENDPOINT,
            response_type=PostV2TweetsResponseBody,
            json=downcast_dict(request_body),
        )