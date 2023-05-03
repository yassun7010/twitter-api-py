from typing import Generic

from twitter_api.client.oauth_session.resources.v2_oauth2_token import (
    V2OAuth2TokenRerources,
    V2Oauth2TokenUrl,
)
from twitter_api.client.oauth_session.twitter_oauth2_session import TwitterOAuth2Session
from twitter_api.types._chainable import Chainable
from twitter_api.types._generic_client import TwitterApiGenericClient
from twitter_api.types.oauth import CallbackUrl


class TwitterOAuth2AccessTokenClient(Chainable, Generic[TwitterApiGenericClient]):
    def __init__(
        self,
        authorization_response_url: CallbackUrl,
        state: str,
        code_verifier: str,
        session: TwitterOAuth2Session[TwitterApiGenericClient],
    ):
        self.authorization_response_url = authorization_response_url
        self.state = state
        self.code_verifier = code_verifier
        self._session = session

    def request(
        self, url: V2Oauth2TokenUrl
    ) -> V2OAuth2TokenRerources[TwitterApiGenericClient]:
        return V2OAuth2TokenRerources(
            authorization_response_url=self.authorization_response_url,
            state=self.state,
            code_verifier=self.code_verifier,
            session=self._session,
        )
