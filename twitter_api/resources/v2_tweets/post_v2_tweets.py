from typing import Literal, NotRequired, Optional, TypedDict, Union

from twitter_api.rate_limit.rate_limit import rate_limit
from twitter_api.resources.api_resources import ApiResources
from twitter_api.types.endpoint import Endpoint
from twitter_api.types.extra_permissive_model import ExtraPermissiveModel
from twitter_api.types.http import Url, downcast_dict
from twitter_api.types.v2_media.media_id import MediaId
from twitter_api.types.v2_place.place_id import PlaceId
from twitter_api.types.v2_scope import oauth2_scopes
from twitter_api.types.v2_tweet.tweet import Tweet
from twitter_api.types.v2_tweet.tweet_id import TweetId
from twitter_api.types.v2_user.user_id import UserId

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


class _BasePostV2TweetsRequestBody(TypedDict):
    direct_message_deep_link: NotRequired[Optional[Url]]
    for_super_followers_only: NotRequired[Optional[bool]]
    geo: NotRequired[Optional[PostV2TweetsGeospatialInformation]]
    poll: NotRequired[Optional[PostV2TweetsPoll]]
    quote_tweet_id: NotRequired[Optional[TweetId]]
    reply: NotRequired[Optional[PostV2TweetsReply]]
    reply_settings: NotRequired[Optional[Literal["mentionedUsers", "following"]]]


class PostV2TweetsRequestBodyMedia(_BasePostV2TweetsRequestBody):
    text: NotRequired[Optional[str]]
    media: PostV2TweetsMedia


class PostV2TweetsRequestBodyText(_BasePostV2TweetsRequestBody):
    text: str
    media: NotRequired[Optional[PostV2TweetsMedia]]


PostV2TweetsRequestBody = Union[
    PostV2TweetsRequestBodyText,
    PostV2TweetsRequestBodyMedia,
]


class PostV2TweetsResponseBody(ExtraPermissiveModel):
    data: Tweet


class PostV2TweetsResources(ApiResources):
    @oauth2_scopes(
        "tweet.read",
        "tweet.write",
        "users.read",
    )
    @rate_limit(ENDPOINT, "user", requests=200, mins=15)
    def post(self, request_body: PostV2TweetsRequestBody) -> PostV2TweetsResponseBody:
        """
        ツイートする。

        refer: https://developer.twitter.com/en/docs/twitter-api/tweets/manage-tweets/api-reference/post-tweets
        """
        return self.request_client.post(
            endpoint=ENDPOINT,
            response_body_type=PostV2TweetsResponseBody,
            body=downcast_dict(request_body),
        )


class AsyncPostV2TweetsResources(PostV2TweetsResources):
    async def post(
        self, request_body: PostV2TweetsRequestBody
    ) -> PostV2TweetsResponseBody:
        return super().post(request_body)
