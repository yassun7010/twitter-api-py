import base64
from typing import Literal, TypedDict

from twitter_api.client.request.request_client import RequestClient
from twitter_api.types.endpoint import Endpoint
from twitter_api.types.extra_permissive_model import ExtraPermissiveModel
from twitter_api.types.oauth import AccessToken, ApiKey, ApiSecret

Uri = Literal["/oauth2/invalidate_token"]

ENDPOINT: Endpoint = Endpoint("POST", "/oauth2/invalidate_token")

PostOauth2InvalidateTokenQueryParameters = TypedDict(
    "PostOauth2InvalidateTokenQueryParameters",
    {
        "access_token": AccessToken,
    },
)


class PostOauth2InvalidateTokenResponseBody(ExtraPermissiveModel):
    access_token: AccessToken


class PostOauth2InvalidateToken:
    def __init__(self, client: RequestClient) -> None:
        self._client = client

    def post(
        self,
        api_key: ApiKey,
        api_secret: ApiSecret,
        query_parameters: PostOauth2InvalidateTokenQueryParameters,
    ) -> PostOauth2InvalidateTokenResponseBody:
        # flake8: noqa E501
        """
        OAuth 2.0 のアプリ用のアクセストークンを削除するために使用する。

        refer: https://developer.twitter.com/en/docs/authentication/api-reference/invalidate_bearer_token
        """

        bearer_token = base64.b64encode(
            f"{api_key}:{api_secret}".encode(),
        )

        return self._client.post(
            endpoint=ENDPOINT,
            response_type=PostOauth2InvalidateTokenResponseBody,
            auth=False,
            headers={
                "Authorization": f"Basic {bearer_token.decode()}",
                "Content-Type": "application/x-www-form-urlencoded",
            },
            query=query_parameters,
        )
