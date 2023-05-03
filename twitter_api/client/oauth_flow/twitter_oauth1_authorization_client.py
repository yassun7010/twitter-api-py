from typing import Generic, Union

from twitter_api.client.oauth_session.resources.oauth1_authenticate import (
    OAuth1AuthenticateSessionResources,
    OauthAuth1enticateUrl,
)
from twitter_api.client.oauth_session.resources.oauth1_authorize import (
    OAuth1AuthorizeSessionResources,
    Oauth1AuthorizeUrl,
)
from twitter_api.client.oauth_session.twitter_oauth1_session import TwitterOAuth1Session
from twitter_api.error import NeverError
from twitter_api.types._chainable import Chainable
from twitter_api.types._generic_client import TwitterApiGenericClient


class TwitterOAuth1AuthorizeClient(Chainable, Generic[TwitterApiGenericClient]):
    def __init__(self, session: TwitterOAuth1Session[TwitterApiGenericClient]) -> None:
        self._session = session

    def request(
        self, url: Union[OauthAuth1enticateUrl, Oauth1AuthorizeUrl]
    ) -> Union[
        OAuth1AuthenticateSessionResources[TwitterApiGenericClient],
        OAuth1AuthorizeSessionResources[TwitterApiGenericClient],
    ]:
        if url == "https://api.twitter.com/oauth/authenticate":
            return OAuth1AuthenticateSessionResources(
                self._session,
            )
        elif url == "https://api.twitter.com/oauth/authorize":
            return OAuth1AuthorizeSessionResources(
                self._session,
            )
        else:
            raise NeverError(url)
