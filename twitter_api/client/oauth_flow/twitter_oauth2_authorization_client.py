from dataclasses import dataclass

from twitter_api.client.oauth_session.resources.oauth2_authorize import (
    OAuth2AuthorizeSessionResources,
    Oauth2AuthorizeUrl,
)
from twitter_api.client.oauth_session.twitter_oauth2_session import TwitterOAuth2Session
from twitter_api.types.chainable import Chainable


@dataclass
class TwitterOAuth2AuthorizeClient(Chainable):
    def __init__(self, session: TwitterOAuth2Session) -> None:
        self._session = session

    def resource(self, url: Oauth2AuthorizeUrl) -> OAuth2AuthorizeSessionResources:
        return OAuth2AuthorizeSessionResources(
            self._session,
        )
