import os

from authlib.integrations.requests_client.oauth1_session import (
    OAuth1Auth,  # pyright: reportMissingImports=false
)
from authlib.integrations.requests_client.oauth2_session import (
    OAuth2Auth,  # pyright: reportMissingImports=false
)

from twitter_api.types.oauth import AccessSecret, AccessToken, ApiKey, ApiSecret, Env

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
        """Bearer 認証を用いてクライアントを作成する。"""

        return TwitterApiRealClient(
            RealRequestClient(
                rate_limit="app",
                auth=OAuth2Auth(
                    token={
                        "access_token": bearer_token,
                        "token_type": "Bearer",
                    }
                ),
            )
        )

    @classmethod
    def from_bearer_token_env(cls, bearer_token="BEARER_TOEKN"):
        """環境変数から、 Bearer 認証を用いてクライアントを作成する。"""

        return cls.from_bearer_token(os.environ[bearer_token])

    @classmethod
    def from_app_auth(
        cls,
        *,
        api_key: ApiKey,
        api_secret: ApiSecret,
    ):
        """アプリ認証を用いてクライアントを作成する。"""
        access_token = (
            TwitterApiRealClient(RealRequestClient(rate_limit="app", auth=None))
            .request("/oauth2/token")
            .post(
                api_key=api_key,
                api_secret=api_secret,
                request_body={"grant_type": "client_credentials"},
            )
            .access_token
        )

        return cls.from_bearer_token(access_token)

    @classmethod
    def from_app_auth_env(
        cls,
        *,
        api_key: Env[ApiKey] = "API_KEY",
        api_secret: Env[ApiSecret] = "API_SECRET",
    ):
        """環境変数から、アプリ認証を用いてクライアントを作成する。"""

        return cls.from_app_auth(
            api_key=os.environ[api_key],
            api_secret=os.environ[api_secret],
        )

    @classmethod
    def from_user_auth(
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
            )
        )

    @classmethod
    def from_user_auth_env(
        cls,
        *,
        api_key: Env[ApiKey] = "API_KEY",
        api_secret: Env[ApiSecret] = "API_SECRET",
        access_token: Env[AccessToken] = "ACCESS_TOKEN",
        access_secret: Env[AccessSecret] = "ACCESS_SECRET",
    ):
        return cls.from_user_auth(
            api_key=os.environ[api_key],
            api_secret=os.environ[api_secret],
            access_token=os.environ[access_token],
            access_secret=os.environ[access_secret],
        )
