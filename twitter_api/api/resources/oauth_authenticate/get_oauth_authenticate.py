from typing import Literal, NotRequired, Optional, TypedDict

from twitter_api.api.resources.api_resources import ApiResources
from twitter_api.client.request.request_client import RequestClient
from twitter_api.types.endpoint import Endpoint
from twitter_api.types.screen_name import ScreenName

ENDPOINT = Endpoint("GET", "https://api.twitter.com/oauth/authenticate")

OauthGetAuthenticateQueryParameters = TypedDict(
    "OauthGetAuthenticateQueryParameters",
    {
        "oauth_token": str,
        "force_login": NotRequired[Optional[bool]],
        "screen_name": NotRequired[Optional[ScreenName]],
    },
)


class OauthGetAuthenticate(ApiResources):
    def get(
        self,
        query: Optional[OauthGetAuthenticateQueryParameters] = None,
    ) -> dict:
        # flake8: noqa E501
        """
        OAuth 1.0a の2番目のステップ。
        ユーザーアクセストークンのセットを生成するために使用する。

        refer: https://developer.twitter.com/en/docs/authentication/api-reference/authenticate
        """
        ...
