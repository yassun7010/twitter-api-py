from authlib.integrations.requests_client.oauth1_session import (
    OAuth1Auth,  # pyright: reportMissingImports=false
)
from authlib.integrations.requests_client.oauth2_session import (
    OAuth2Auth,  # pyright: reportMissingImports=false
)

from twitter_api.types.oauth import AccessSecret, AccessToken, ApiKey, ApiSecret

from .request.real_request_client import RealRequestClient
from .request.request_client import RequestClient
from .twitter_api_client import TwitterApiClient


class TwitterApiRealClient(TwitterApiClient):
    """
    Twitter API V2 を操作するためのクライアント

    TwitterApiClient から生成されるクラスは、このクラスを継承する。
    """

    def __init__(
        self,
        request_client: RealRequestClient,
    ) -> None:
        self._client = request_client

    @property
    def _request_client(self) -> RequestClient:
        return self._client

    @classmethod
    def from_bearer_token(cls, bearer_token: str):
        return TwitterApiRealClient(
            RealRequestClient(
                rate_limit="app",
                auth=OAuth2Auth(
                    token={
                        "access_token": bearer_token,
                        "token_type": "Bearer",
                    }
                ),
                oauth_version="2.0",
            ),
        )

    @classmethod
    def from_app_auth_v2(
        cls,
        *,
        api_key: ApiKey,
        api_secret: ApiSecret,
    ):
        access_token = (
            TwitterApiRealClient(
                RealRequestClient(
                    rate_limit="app",
                    auth=None,
                    oauth_version="2.0",
                ),
            )
            .request("/oauth2/token")
            .post(
                api_key=api_key,
                api_secret=api_secret,
                query_parameters={"grant_type": "client_credentials"},
            )
            .access_token
        )

        return cls.from_bearer_token(access_token)

    @classmethod
    def from_user_auth_v1(
        cls,
        *,
        api_key: ApiKey,
        api_secret: ApiSecret,
        access_token: AccessToken,
        access_secret: AccessSecret,
    ):
        return TwitterApiRealClient(
            RealRequestClient(
                rate_limit="user",
                auth=OAuth1Auth(
                    client_id=api_key,
                    client_secret=api_secret,
                    token=access_token,
                    token_secret=access_secret,
                ),
                oauth_version="1.0a",
            ),
        )
