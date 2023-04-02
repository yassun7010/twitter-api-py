import base64
from typing import Literal, TypedDict

from twitter_api.client.request.request_client import RequestClient
from twitter_api.error import TwitterApiOAuthVersionWrong
from twitter_api.types.endpoint import Endpoint
from twitter_api.types.extra_permissive_model import ExtraPermissiveModel
from twitter_api.types.http import downcast_dict
from twitter_api.types.oauth import AccessToken, ApiKey, ApiSecret

Url = Literal["https://api.twitter.com/oauth2/invalidate_token"]

ENDPOINT: Endpoint = Endpoint("POST", "https://api.twitter.com/oauth2/invalidate_token")

Oauth2PostInvalidateTokenQueryParameters = TypedDict(
    "Oauth2PostInvalidateTokenQueryParameters",
    {
        "access_token": AccessToken,
    },
)


class Oauth2PostInvalidateTokenResponseBody(ExtraPermissiveModel):
    access_token: AccessToken


class Oauth2PostInvalidateToken:
    def __init__(self, client: RequestClient) -> None:
        self._client = client

    def post(
        self,
        api_key: ApiKey,
        api_secret: ApiSecret,
        query: Oauth2PostInvalidateTokenQueryParameters,
    ) -> Oauth2PostInvalidateTokenResponseBody:
        # flake8: noqa E501
        """
        OAuth 2.0 のアプリ用のアクセストークンを削除するために使用する。

        refer: https://developer.twitter.com/en/docs/authentication/api-reference/invalidate_bearer_token
        """

        if self._client.oauth_version != "2.0":
            raise TwitterApiOAuthVersionWrong(
                version=self._client.oauth_version, expected_version="2.0"
            )

        bearer_token = base64.b64encode(
            f"{api_key}:{api_secret}".encode(),
        )

        return self._client.post(
            endpoint=ENDPOINT,
            response_type=Oauth2PostInvalidateTokenResponseBody,
            auth=False,
            headers={
                "Authorization": f"Basic {bearer_token.decode()}",
                "Content-Type": "application/x-www-form-urlencoded",
            },
            query=downcast_dict(query),
        )
