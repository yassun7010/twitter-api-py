from typing import Literal, TypedDict


from twitter_api.client.request.request_client import RequestClient
import base64
from twitter_api.types.endpoint import Endpoint
from twitter_api.types.extra_permissive_model import ExtraPermissiveModel
from twitter_api.types.oauth import (
    AccessToken,
    ConsumerKey,
    ConsumerSecret,
)

Uri = Literal["/oauth2/invalidate_token"]

ENDPOINT: Endpoint = Endpoint("POST", "/oauth2/invalidate_token")


class PostOauth2InvalidateTokenResponseBody(ExtraPermissiveModel):
    access_token: AccessToken


class PostOauth2InvalidateToken:
    def __init__(self, client: RequestClient) -> None:
        self._client = client

    def post(
        self,
        consumer_key: ConsumerKey,
        consumer_secret: ConsumerSecret,
    ) -> PostOauth2InvalidateTokenResponseBody:
        # flake8: noqa E501
        """
        OAuth 2.0 のアプリ用のアクセストークンを削除するために使用する。

        refer: https://developer.twitter.com/en/docs/authentication/api-reference/invalidate_bearer_token
        """

        bearer_token = base64.b64encode(
            f"{consumer_key}:{consumer_secret}".encode()
        )

        return self._client.post(
            endpoint=ENDPOINT,
            response_type=PostOauth2InvalidateTokenResponseBody,
            headers={
                "Authorization": f"Basic {bearer_token.decode()}",
                "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
            },
        )
