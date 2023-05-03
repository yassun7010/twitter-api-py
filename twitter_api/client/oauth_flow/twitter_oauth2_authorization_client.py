from dataclasses import dataclass
from typing import Generic

from twitter_api.client.oauth_session.resources.oauth2_authorize import (
    OAuth2AuthorizeSessionResources,
    Oauth2AuthorizeUrl,
)
from twitter_api.client.oauth_session.twitter_oauth2_session import TwitterOAuth2Session
from twitter_api.types._chainable import Chainable
from twitter_api.types._generic_client import TwitterApiGenericClient


@dataclass
class TwitterOAuth2AuthorizeClient(Chainable, Generic[TwitterApiGenericClient]):
    def __init__(self, session: TwitterOAuth2Session[TwitterApiGenericClient]) -> None:
        self._session = session

    def request(
        self, url: Oauth2AuthorizeUrl
    ) -> OAuth2AuthorizeSessionResources[TwitterApiGenericClient]:
        return OAuth2AuthorizeSessionResources(
            self._session,
        )
