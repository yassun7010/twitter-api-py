from typing import TypedDict

from twitter_api.api.v2.types.user.user_id import UserId
from twitter_api.client.types.api_resources import ApiResources
from twitter_api.rate_limit.rate_limit_decorator import rate_limit
from twitter_api.types.endpoint import Endpoint
from twitter_api.types.extra_permissive_model import ExtraPermissiveModel
from twitter_api.types.http import downcast_dict

ENDPOINT = Endpoint("POST", "https://api.twitter.com/2/users/:id/following")

V2PostUserFollowingRequestBody = TypedDict(
    "V2PostUserFollowingRequestBody",
    {
        "target_user_id": UserId,
    },
)


class V2PostUserFollowingResponseBodyData(ExtraPermissiveModel):
    following: bool
    pending_follow: bool


class V2PostUserFollowingResponseBody(ExtraPermissiveModel):
    data: V2PostUserFollowingResponseBodyData


class V2PostUserFollowingResources(ApiResources):
    @rate_limit(ENDPOINT, "user", requests=50, mins=15)
    def post(
        self,
        id: UserId,
        request_body: V2PostUserFollowingRequestBody,
    ) -> V2PostUserFollowingResponseBody:
        # flake8: noqa E501
        """
        ユーザをフォローする。

        refer: https://developer.twitter.com/en/docs/twitter-api/users/follows/api-reference/post-users-source_user_id-following
        """
        return self.request_client.post(
            endpoint=ENDPOINT,
            url=ENDPOINT.url.replace(":id", id),
            json=downcast_dict(request_body),
            response_type=V2PostUserFollowingResponseBody,
        )
