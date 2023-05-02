import base64
from typing import TypedDict

from twitter_api.error import TwitterApiOAuthVersionWrong
from twitter_api.resources.api_resources import ApiResources
from twitter_api.types.endpoint import Endpoint
from twitter_api.types.extra_permissive_model import ExtraPermissiveModel
from twitter_api.types.http import downcast_dict
from twitter_api.types.oauth import AccessToken, ApiKey, ApiSecret

ENDPOINT: Endpoint = Endpoint("POST", "https://api.twitter.com/oauth2/invalidate_token")

PostOauth2InvalidateTokenQueryParameters = TypedDict(
    "PostOauth2InvalidateTokenQueryParameters",
    {
        "access_token": AccessToken,
    },
)


class PostOauth2InvalidateTokenResponseBody(ExtraPermissiveModel):
    access_token: AccessToken


class PostOauth2InvalidateTokenResources(ApiResources):
    def post(
        self,
        api_key: ApiKey,
        api_secret: ApiSecret,
        query: PostOauth2InvalidateTokenQueryParameters,
    ) -> PostOauth2InvalidateTokenResponseBody:
        """
        OAuth 2.0 のアプリ用のアクセストークンを削除するために使用する。

        refer: https://developer.twitter.com/en/docs/authentication/api-reference/invalidate_bearer_token
        """

        if self.request_client.oauth_version != "2.0":
            raise TwitterApiOAuthVersionWrong(
                version=self.request_client.oauth_version, expected_version="2.0"
            )

        bearer_token = base64.b64encode(
            f"{api_key}:{api_secret}".encode(),
        )

        return self.request_client.post(
            endpoint=ENDPOINT,
            response_body_type=PostOauth2InvalidateTokenResponseBody,
            auth=False,
            headers={
                "Authorization": f"Basic {bearer_token.decode()}",
                "Content-Type": "application/x-www-form-urlencoded",
            },
            query=downcast_dict(query),
        )


class AsyncPostOauth2InvalidateTokenResources(PostOauth2InvalidateTokenResources):
    async def post(
        self,
        api_key: ApiKey,
        api_secret: ApiSecret,
        query: PostOauth2InvalidateTokenQueryParameters,
    ) -> PostOauth2InvalidateTokenResponseBody:
        return super().post(
            api_key,
            api_secret,
            query,
        )
