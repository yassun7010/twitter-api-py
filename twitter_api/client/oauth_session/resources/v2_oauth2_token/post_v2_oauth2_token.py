from typing import Generic

from twitter_api.client.oauth_session.resources.session_resources import (
    OAuth2SessionResources,
)
from twitter_api.client.oauth_session.twitter_oauth2_session import TwitterOAuth2Session
from twitter_api.types._generic_client import TwitterApiGenericClient
from twitter_api.types.endpoint import Endpoint
from twitter_api.types.oauth import CallbackUrl
from twitter_api.types.oauth2.oauth2_access_token import OAuth2AccessToken

ENDPOINT = Endpoint("POST", "https://api.twitter.com/2/oauth2/token")


class PostV2OAuth2TokenRerources(
    OAuth2SessionResources, Generic[TwitterApiGenericClient]
):
    def __init__(
        self,
        authorization_response_url: CallbackUrl,
        state: str,
        code_verifier: str,
        session: TwitterOAuth2Session[TwitterApiGenericClient],
    ) -> None:
        self._authorization_response_url = authorization_response_url
        self._state = state
        self._code_verifier = code_verifier
        super().__init__(session)

    def post(self) -> OAuth2AccessToken[TwitterApiGenericClient]:
        """
        OAuth2.0 のユーザ認証（PKCE）の最後のステップ。認証のトークンを発行する。

        API 専用のページはドキュメントに存在しない。

        refer: https://developer.twitter.com/en/docs/authentication/oauth-2-0/authorization-code
        """
        return self._session.fetch_token(
            authorization_response_url=self._authorization_response_url,
            state=self._state,
            code_verifier=self._code_verifier,
        )
