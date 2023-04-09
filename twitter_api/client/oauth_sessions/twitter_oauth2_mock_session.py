from datetime import datetime

from twitter_api.api.types.v2_oauth2.oauth2_access_token import OAuth2AccessToken
from twitter_api.api.types.v2_scope import Scope
from twitter_api.client.oauth_sessions.twitter_oauth2_session import (
    TwitterOAuth2Session,
)
from twitter_api.types.oauth import CallbackUrl


class TwitterOAuth2MockSession(TwitterOAuth2Session):
    def __init__(self, *, scope: list[Scope]) -> None:
        self._scope = scope

    def generate_authorization_url(self):
        from twitter_api.api.types.v2_oauth2.oauth2_authorization import (
            OAuth2Authorization,
        )

        return OAuth2Authorization(
            authorization_url="https://authorization.url.com",
            state="state",
            code_verifier="code_verifier",
            session=self,
        )

    def fetch_token(
        self,
        authorization_response_url: CallbackUrl,
        state: str,
        code_verifier: str,
    ) -> OAuth2AccessToken:
        expires_in = 7200
        return OAuth2AccessToken(
            token_type="bearer",
            expires_in=expires_in,
            expires_at=int(datetime.now().timestamp()) + expires_in,
            access_token="access_token",
            scope=self._scope,
        )
