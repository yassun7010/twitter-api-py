from typing import Literal, NotRequired, Optional, TypedDict

from authlib.integrations.requests_client.oauth1_session import (
    OAuth1Session,  # pyright: reportMissingImports=false
)

from twitter_api.client.request.request_client import RequestClient
from twitter_api.error import TwitterApiOAuthVersionWrong
from twitter_api.types.endpoint import Endpoint
from twitter_api.types.extra_permissive_model import ExtraPermissiveModel
from twitter_api.types.oauth import ApiKey, ApiSecret, OAuthToken, OAuthTokenSecret

Uri = Literal["/oauth/request_token"]

ENDPOINT: Endpoint = Endpoint("POST", "/oauth/request_token")

OauthPostRequestTokenQueryParameters = TypedDict(
    "OauthPostRequestTokenQueryParameters",
    {
        "oauth_callback": str,
        "x_auth_access_type": NotRequired[Optional[Literal["read", "write"]]],
    },
)


class OauthPostRequestTokenResponseBody(ExtraPermissiveModel):
    oauth_token: OAuthToken
    oauth_token_secret: OAuthTokenSecret
    oauth_callback_confirmed: bool


class OauthPostRequestToken:
    def __init__(
        self,
        client: RequestClient,
    ) -> None:
        self._client = client

    def post(
        self,
        api_key: ApiKey,
        api_secret: ApiSecret,
        query_parameters: OauthPostRequestTokenQueryParameters,
    ) -> OauthPostRequestTokenResponseBody:
        # flake8: noqa E501
        """
        OAuth 1.0a の最初のステップ。
        ユーザーアクセストークンのセットを生成するために使用する。

        refer: https://developer.twitter.com/en/docs/authentication/api-reference/request_token
        """
        if self._client.oauth_version != "1.0a":
            raise TwitterApiOAuthVersionWrong(
                version=self._client.oauth_version, expected_version="1.0a"
            )
        # NOTE: このコードは成功するが、さらなる調査が必要。
        #
        # return OauthPostRequestTokenResponseBody(
        #     **OAuth1Session(
        #         client_id=api_key,
        #         client_secret=api_secret,
        #         callback_uri=query_parameters["oauth_callback"],
        #     ).fetch_request_token("https://api.twitter.com/oauth/request_token")
        # )

        return self._client.post(
            endpoint=ENDPOINT,
            response_type=OauthPostRequestTokenResponseBody,
            query=query_parameters,  # type: ignore
        )
