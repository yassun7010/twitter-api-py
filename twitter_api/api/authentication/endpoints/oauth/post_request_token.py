from typing import Literal, NotRequired, Optional, TypedDict

from twitter_api.client.request.request_client import RequestClient
from twitter_api.types.endpoint import Endpoint
from twitter_api.types.extra_permissive_model import ExtraPermissiveModel
from twitter_api.types.oauth import OAuthToken, OAuthTokenSecret

Uri = Literal["/oauth/request_token"]

ENDPOINT: Endpoint = Endpoint("POST", "/oauth/request_token")

OauthPostRequestTokenQueryParameters = TypedDict(
    "OauthPostRequestTokenQueryParameters",
    {
        "oauth_callback": str,
        "x_auth_access_type": NotRequired[Optional[str]],
    },
)


class OauthPostRequestTokenResponseBody(ExtraPermissiveModel):
    oauth_token: OAuthToken
    oauth_token_secret: OAuthTokenSecret
    oauth_callback_confirmed: bool


class OauthPostRequestToken:
    def __init__(self, client: RequestClient) -> None:
        self._client = client

    def post(
        self,
        headers: OauthPostRequestTokenQueryParameters,
    ) -> OauthPostRequestTokenResponseBody:
        # flake8: noqa E501
        """
        OAuth 1.0a の最初のステップ。
        ユーザーアクセストークンのセットを生成するために使用する。

        refer: https://developer.twitter.com/en/docs/authentication/api-reference/request_token
        """
        return self._client.post(
            endpoint=ENDPOINT,
            response_type=OauthPostRequestTokenResponseBody,
            headers=headers,  # type: ignore
        )
