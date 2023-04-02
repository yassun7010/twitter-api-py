import base64
from typing import Literal, TypedDict

from twitter_api.client.request.request_client import RequestClient
from twitter_api.error import TwitterApiOAuthVersionWrong
from twitter_api.types.endpoint import Endpoint
from twitter_api.types.extra_permissive_model import ExtraPermissiveModel
from twitter_api.types.http import downcast_dict
from twitter_api.types.oauth import AccessToken, ApiKey, ApiSecret

Uri = Literal["https://api.twitter.com/oauth2/token"]

ENDPOINT: Endpoint = Endpoint("POST", "https://api.twitter.com/oauth2/token")


class Oauth2PostTokenQueryParameters(TypedDict):
    grant_type: Literal["client_credentials"]


class Oauth2PostTokenResponseBody(ExtraPermissiveModel):
    token_type: Literal["bearer"]
    access_token: AccessToken


class Oauth2PostToken:
    def __init__(self, client: RequestClient) -> None:
        self._client = client

    def post(
        self,
        api_key: ApiKey,
        api_secret: ApiSecret,
        query_parameters: Oauth2PostTokenQueryParameters,
    ) -> Oauth2PostTokenResponseBody:
        # flake8: noqa E501
        """
        OAuth 2.0 のアプリ用のアクセストークンのセットを生成するために使用する。

        refer: https://developer.twitter.com/en/docs/authentication/api-reference/token
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
            response_type=Oauth2PostTokenResponseBody,
            auth=False,
            headers={
                "Authorization": f"Basic {bearer_token.decode()}",
                "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
            },
            query=downcast_dict(query_parameters),
        )
