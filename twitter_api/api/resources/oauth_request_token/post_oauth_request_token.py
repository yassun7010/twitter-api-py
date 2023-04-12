from typing import Literal, NotRequired, Optional, TypedDict

from twitter_api.api.resources.api_resources import ApiResources
from twitter_api.error import TwitterApiOAuthVersionWrong
from twitter_api.types.endpoint import Endpoint
from twitter_api.types.extra_permissive_model import ExtraPermissiveModel
from twitter_api.types.oauth import ApiKey, ApiSecret, OAuthToken, OAuthTokenSecret

ENDPOINT: Endpoint = Endpoint("POST", "https://api.twitter.com/oauth/request_token")

PostOauthRequestTokenQueryParameters = TypedDict(
    "PostOauthRequestTokenQueryParameters",
    {
        "oauth_callback": str,
        "x_auth_access_type": NotRequired[Optional[Literal["read", "write"]]],
    },
)


class PostOauthRequestTokenResponseBody(ExtraPermissiveModel):
    oauth_token: OAuthToken
    oauth_token_secret: OAuthTokenSecret
    oauth_callback_confirmed: bool


class PostOauthRequestTokenResources(ApiResources):
    def post(
        self,
        api_key: ApiKey,
        api_secret: ApiSecret,
        query: PostOauthRequestTokenQueryParameters,
    ) -> PostOauthRequestTokenResponseBody:
        """
        OAuth 1.0a の最初のステップ。
        ユーザーアクセストークンのセットを生成するために使用する。

        refer: https://developer.twitter.com/en/docs/authentication/api-reference/request_token
        """
        if self.request_client.oauth_version != "1.0a":
            raise TwitterApiOAuthVersionWrong(
                version=self.request_client.oauth_version, expected_version="1.0a"
            )

        # NOTE: このコードは成功するが、さらなる調査が必要。
        #
        # return PostOauthRequestTokenResponseBody(
        #     **OAuth1Session(
        #         client_id=api_key,
        #         client_secret=api_secret,
        #         callback_uri=query["oauth_callback"],
        #     ).fetch_request_token("https://api.twitter.com/oauth/request_token")
        # )

        return self.request_client.post(
            endpoint=ENDPOINT,
            response_type=PostOauthRequestTokenResponseBody,
            query=query,  # type: ignore
        )
