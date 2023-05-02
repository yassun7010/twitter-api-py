from typing import TypedDict

from twitter_api.rate_limit.rate_limit import rate_limit
from twitter_api.resources.api_resources import ApiResources
from twitter_api.types.endpoint import Endpoint
from twitter_api.types.extra_permissive_model import ExtraPermissiveModel
from twitter_api.types.http import downcast_dict
from twitter_api.types.v2_scope import oauth2_scopes
from twitter_api.types.v2_user.user_id import UserId

ENDPOINT = Endpoint("POST", "https://api.twitter.com/2/users/:id/following")

PostV2UserFollowingRequestBody = TypedDict(
    "PostV2UserFollowingRequestBody",
    {
        "target_user_id": UserId,
    },
)


class PostV2UserFollowingResponseBodyData(ExtraPermissiveModel):
    following: bool
    pending_follow: bool


class PostV2UserFollowingResponseBody(ExtraPermissiveModel):
    data: PostV2UserFollowingResponseBodyData


class PostV2UserFollowingResources(ApiResources):
    @oauth2_scopes(
        "tweet.read",
        "users.read",
        "follows.write",
    )
    @rate_limit(ENDPOINT, "user", requests=50, mins=15)
    def post(
        self,
        id: UserId,
        request_body: PostV2UserFollowingRequestBody,
    ) -> PostV2UserFollowingResponseBody:
        """
        ユーザをフォローする。

        refer: https://developer.twitter.com/en/docs/twitter-api/users/follows/api-reference/post-users-source_user_id-following
        """
        return self.request_client.post(
            endpoint=ENDPOINT,
            url=ENDPOINT.url.replace(":id", id),
            body=downcast_dict(request_body),
            response_body_type=PostV2UserFollowingResponseBody,
        )


class AsyncPostV2UserFollowingResources(PostV2UserFollowingResources):
    async def post(
        self,
        id: UserId,
        request_body: PostV2UserFollowingRequestBody,
    ) -> PostV2UserFollowingResponseBody:
        return super().post(id, request_body)
