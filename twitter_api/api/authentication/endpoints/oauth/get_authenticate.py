from typing import Literal, NotRequired, Optional, TypedDict

from twitter_api.client.request.request_client import RequestClient
from twitter_api.types.endpoint import Endpoint
from twitter_api.types.screen_name import ScreenName
from twitter_api.utils.ratelimit import rate_limit

Uri = Literal["/oauth/authenticate"]

ENDPOINT = Endpoint("GET", "/oauth/authenticate")

GetOauthAuthenticateQueryParameters = TypedDict(
    "GetOauthAuthenticateQueryParameters",
    {
        "oauth_token": str,
        "force_login": NotRequired[Optional[bool]],
        "screen_name": NotRequired[Optional[ScreenName]],
    },
)


class GetOauthAuthenticate:
    def __init__(self, client: RequestClient) -> None:
        self._client = client

    def get(
        self,
        query: Optional[GetOauthAuthenticateQueryParameters] = None,
    ) -> dict:
        # flake8: noqa E501
        """
        OAuth 1.0a の2番目のステップ。
        ユーザーアクセストークンのセットを生成するために使用する。

        refer: https://developer.twitter.com/en/docs/authentication/api-reference/authenticate
        """
        ...
