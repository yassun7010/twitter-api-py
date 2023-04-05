from typing import TypedDict

from twitter_api.api.resources.api_resources import ApiResources
from twitter_api.api.types.v2_tweet.tweet_id import TweetId
from twitter_api.api.types.v2_user.user_id import UserId
from twitter_api.rate_limit.rate_limit_decorator import rate_limit
from twitter_api.types.endpoint import Endpoint
from twitter_api.types.extra_permissive_model import ExtraPermissiveModel
from twitter_api.types.http import downcast_dict

ENDPOINT = Endpoint("POST", "https://api.twitter.com/2/users/:id/retweets")

PostV2UserRetweetsRequestBody = TypedDict(
    "PostV2UserRetweetsRequestBody",
    {
        "tweet_id": TweetId,
    },
)


class PostV2UserRetweetsResponseBodyData(ExtraPermissiveModel):
    retweeted: bool


class PostV2UserRetweetsResponseBody(ExtraPermissiveModel):
    data: PostV2UserRetweetsResponseBodyData


class PostV2UserRetweetsResources(ApiResources):
    @rate_limit(ENDPOINT, "user", requests=50, mins=15)
    def post(
        self,
        id: UserId,
        request_body: PostV2UserRetweetsRequestBody,
    ) -> PostV2UserRetweetsResponseBody:
        # flake8: noqa E501
        """
        ユーザをリツイートする。

        refer: https://developer.twitter.com/en/docs/twitter-api/tweets/retweets/api-reference/post-users-id-retweets
        """
        return self.request_client.post(
            endpoint=ENDPOINT,
            url=ENDPOINT.url.replace(":id", id),
            json=downcast_dict(request_body),
            response_type=PostV2UserRetweetsResponseBody,
        )