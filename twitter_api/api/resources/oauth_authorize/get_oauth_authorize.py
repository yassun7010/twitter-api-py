from typing import NotRequired, Optional, TypedDict

from twitter_api.client.request.request_client import RequestClient
from twitter_api.types.endpoint import Endpoint
from twitter_api.types.screen_name import ScreenName

ENDPOINT = Endpoint("GET", "https://api.twitter.com/oauth/authorize")

GetOauthAuthorizeQueryParameters = TypedDict(
    "GetOauthAuthorizeQueryParameters",
    {
        "oauth_token": str,
        "force_login": NotRequired[Optional[bool]],
        "screen_name": NotRequired[Optional[ScreenName]],
    },
)


class GetOauthAuthorizeResources(RequestClient):
    def get(
        self,
        query: Optional[GetOauthAuthorizeQueryParameters] = None,
    ) -> dict:
        # flake8: noqa E501
        """
        OAuth 1.0a の2番目のステップ。
        ユーザーアクセストークンのセットを生成するために使用する。

        refer: https://developer.twitter.com/en/docs/authentication/api-reference/authorize
        """
        ...
