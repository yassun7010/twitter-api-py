from typing import Any

from authlib.integrations.requests_client.oauth2_session import OAuth2Session

from twitter_api.api.types.v2_oauth2.oauth2_access_token import OAuth2AcccessToken
from twitter_api.types.chainable import Chainable
from twitter_api.types.http import Url
from twitter_api.types.oauth import CallbackUrl


class PostV2OAuth2TokenRerources(Chainable):
    def __init__(
        self,
        url: Url,
        authorization_response_url: CallbackUrl,
        state: str,
        code_verifier: str,
        session: OAuth2Session,
    ) -> None:
        self._url = url
        self._authorization_response_url = authorization_response_url
        self._state = state
        self._code_verifier = code_verifier
        self._session = session

    def post(self) -> OAuth2AcccessToken:
        access_token = self._session.fetch_token(
            url=self._url,
            authorization_response=self._authorization_response_url,
            state=self._state,
            code_verifier=self._code_verifier,
        )
        scope: Any = access_token.pop("scope", "").split(" ")

        return OAuth2AcccessToken(
            scope=scope,
            **access_token,
        )
