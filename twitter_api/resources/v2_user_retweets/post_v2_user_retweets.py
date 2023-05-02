from typing import TypedDict

from twitter_api.rate_limit.rate_limit import rate_limit
from twitter_api.resources.api_resources import ApiResources
from twitter_api.types.endpoint import Endpoint
from twitter_api.types.extra_permissive_model import ExtraPermissiveModel
from twitter_api.types.http import downcast_dict
from twitter_api.types.v2_scope import oauth2_scopes
from twitter_api.types.v2_tweet.tweet_id import TweetId
from twitter_api.types.v2_user.user_id import UserId

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
    @oauth2_scopes(
        "tweet.read",
        "tweet.write",
        "users.read",
    )
    @rate_limit(ENDPOINT, "user", requests=50, mins=15)
    def post(
        self,
        id: UserId,
        request_body: PostV2UserRetweetsRequestBody,
    ) -> PostV2UserRetweetsResponseBody:
        """
        ユーザをリツイートする。

        refer: https://developer.twitter.com/en/docs/twitter-api/tweets/retweets/api-reference/post-users-id-retweets
        """
        return self.request_client.post(
            endpoint=ENDPOINT,
            url=ENDPOINT.url.replace(":id", id),
            body=downcast_dict(request_body),
            response_body_type=PostV2UserRetweetsResponseBody,
        )


class AsyncPostV2UserRetweetsResources(PostV2UserRetweetsResources):
    async def post(
        self,
        id: UserId,
        request_body: PostV2UserRetweetsRequestBody,
    ) -> PostV2UserRetweetsResponseBody:
        return super().post(id, request_body)
