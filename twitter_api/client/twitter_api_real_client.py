from typing import Optional

from authlib.integrations.requests_client.oauth1_session import (
    OAuth1Auth,  # pyright: reportMissingImports=false
)
from authlib.integrations.requests_client.oauth2_session import (
    OAuth2Auth,  # pyright: reportMissingImports=false
)

from twitter_api.rate_limit.manager.rate_limit_manager import RateLimitManager
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
    def from_bearer_token(
        cls,
        bearer_token: str,
        rate_limit_manager: Optional[RateLimitManager] = None,
    ):
        return TwitterApiRealClient(
            RealRequestClient(
                auth=OAuth2Auth(
                    token={
                        "access_token": bearer_token,
                        "token_type": "Bearer",
                    }
                ),
                oauth_version="2.0",
                rate_limit_target="app",
                rate_limit_manager=rate_limit_manager,
            ),
        )

    @classmethod
    def from_app_auth_v2(
        cls,
        *,
        api_key: ApiKey,
        api_secret: ApiSecret,
        rate_limit_manager: Optional[RateLimitManager] = None,
    ):
        client = TwitterApiRealClient(
            RealRequestClient(
                auth=None,
                oauth_version="2.0",
                rate_limit_target="app",
                rate_limit_manager=rate_limit_manager,
            ),
        )

        client._client._auth = OAuth2Auth(
            token={
                "access_token": (
                    client.request("https://api.twitter.com/oauth2/token")
                    .post(
                        api_key=api_key,
                        api_secret=api_secret,
                        query={"grant_type": "client_credentials"},
                    )
                    .access_token
                ),
                "token_type": "Bearer",
            }
        )

        return client

    @classmethod
    def from_user_auth_v1(
        cls,
        *,
        api_key: ApiKey,
        api_secret: ApiSecret,
        access_token: AccessToken,
        access_secret: AccessSecret,
        rate_limit_manager: Optional[RateLimitManager] = None,
    ):
        return TwitterApiRealClient(
            RealRequestClient(
                auth=OAuth1Auth(
                    client_id=api_key,
                    client_secret=api_secret,
                    token=access_token,
                    token_secret=access_secret,
                ),
                oauth_version="1.0a",
                rate_limit_target="user",
                rate_limit_manager=rate_limit_manager,
            ),
        )
