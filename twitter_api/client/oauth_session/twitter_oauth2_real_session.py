from typing import Any, Optional

from authlib.integrations.requests_client.oauth2_session import (  # pyright: reportMissingImports=false
    OAuth2Session,
)

from twitter_api.api.resources.oauth2_authorize import Oauth2AuthorizeUrl
from twitter_api.api.resources.v2_oauth2_token import V2Oauth2TokenUrl
from twitter_api.api.types.v2_oauth2.oauth2_access_token import OAuth2AccessToken
from twitter_api.api.types.v2_oauth2.oauth2_authorization import OAuth2Authorization
from twitter_api.api.types.v2_scope import Scope
from twitter_api.client.oauth_session.twitter_oauth2_session import TwitterOAuth2Session
from twitter_api.types.oauth import CallbackUrl, ClientId, ClientSecret
from twitter_api.utils.oauth import generate_code_verifier


class TwitterOAuth2RealSession(TwitterOAuth2Session):
    def __init__(
        self,
        *,
        client_id: ClientId,
        client_secret: ClientSecret,
        callback_url: CallbackUrl,
        scope: Optional[list[Scope]] = None,
    ) -> None:
        self._session = OAuth2Session(
            client_id=client_id,
            client_secret=client_secret,
            redirect_uri=callback_url,
            scope=scope,
            code_challenge_method="S256",
        )

    def generate_authorization_url(self) -> OAuth2Authorization:
        url: Oauth2AuthorizeUrl = "https://twitter.com/i/oauth2/authorize"
        code_verifier = generate_code_verifier()

        authorization_url, state = self._session.create_authorization_url(
            url, code_verifier=code_verifier
        )

        return OAuth2Authorization(
            authorization_url=authorization_url,
            state=state,
            code_verifier=code_verifier,
            session=self,
        )

    def fetch_token(
        self,
        authorization_response_url: CallbackUrl,
        state: str,
        code_verifier: str,
    ) -> OAuth2AccessToken:
        url: V2Oauth2TokenUrl = "https://api.twitter.com/2/oauth2/token"

        response = self._session.fetch_token(
            url=url,
            authorization_response=authorization_response_url,
            state=state,
            code_verifier=code_verifier,
        )

        scope: Any = response.pop("scope", "").split(" ")

        return OAuth2AccessToken(
            scope=scope,
            **response,
        )
