from typing import NotRequired, Optional, TypedDict

from twitter_api.api.resources.api_resources import ApiResources
from twitter_api.types.endpoint import Endpoint
from twitter_api.types.screen_name import ScreenName

ENDPOINT = Endpoint("GET", "https://api.twitter.com/oauth/authenticate")

GetOauthAuthenticateQueryParameters = TypedDict(
    "GetOauthAuthenticateQueryParameters",
    {
        "oauth_token": str,
        "force_login": NotRequired[Optional[bool]],
        "screen_name": NotRequired[Optional[ScreenName]],
    },
)


class GetOauthAuthenticate(ApiResources):
    def get(
        self,
        query: Optional[GetOauthAuthenticateQueryParameters] = None,
    ) -> dict:
        """
        OAuth 1.0a の2番目のステップ。
        ユーザーアクセストークンのセットを生成するために使用する。

        refer: https://developer.twitter.com/en/docs/authentication/api-reference/authenticate
        """
        ...
