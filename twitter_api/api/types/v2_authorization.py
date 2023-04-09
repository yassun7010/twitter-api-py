from dataclasses import dataclass

from twitter_api.api.resources.oauth2_authorize import Oauth2AuthorizeUrl
from twitter_api.api.types.v2_oauth2.generate_authorization_url import (
    GenerateAuthorizationUrl,
)
from twitter_api.client.sessions.twitter_oauth2_session import TwitterOAuth2Session
from twitter_api.types.chainable import Chainable


@dataclass
class OAuthV2AuthorizeClient(Chainable):
    def __init__(self, session: TwitterOAuth2Session) -> None:
        self._session = session

    def request(self, url: Oauth2AuthorizeUrl) -> GenerateAuthorizationUrl:
        return GenerateAuthorizationUrl(
            url,
            self._session,
        )
