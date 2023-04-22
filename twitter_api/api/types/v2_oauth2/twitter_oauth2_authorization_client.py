from dataclasses import dataclass

from twitter_api.api.resources.oauth2_authorize import Oauth2AuthorizeUrl
from twitter_api.api.resources.oauth2_authorize.generate_authorization_url import (
    GenerateAuthorizationUrlOAuth2Session,
)
from twitter_api.client.oauth_session.twitter_oauth2_session import TwitterOAuth2Session
from twitter_api.types.chainable import Chainable


@dataclass
class TwitterOAuth2AuthorizeClient(Chainable):
    def __init__(self, session: TwitterOAuth2Session) -> None:
        self._session = session

    def resource(
        self, url: Oauth2AuthorizeUrl
    ) -> GenerateAuthorizationUrlOAuth2Session:
        return GenerateAuthorizationUrlOAuth2Session(
            url,
            self._session,
        )
