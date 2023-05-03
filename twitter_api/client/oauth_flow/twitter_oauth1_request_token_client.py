from typing import Generic

from twitter_api.client.oauth_session.resources.oauth1_request_token import (
    OAuth1RequestTokenSessionResources,
    Oauth1RequestTokenUrl,
)
from twitter_api.client.oauth_session.twitter_oauth1_session import TwitterOAuth1Session
from twitter_api.types._chainable import Chainable
from twitter_api.types._generic_client import TwitterApiGenericClient


class TwitterOAuth1RequestTokenClient(Chainable, Generic[TwitterApiGenericClient]):
    def __init__(self, session: TwitterOAuth1Session[TwitterApiGenericClient]) -> None:
        self._session = session

    def request(
        self, url: Oauth1RequestTokenUrl
    ) -> OAuth1RequestTokenSessionResources[TwitterApiGenericClient]:
        return OAuth1RequestTokenSessionResources(
            self._session,
        )
