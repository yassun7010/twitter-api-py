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
from twitter_api.types.chainable import Chainable


class TwitterOAuth1AuthorizeClient(Chainable):
    def __init__(self, session: TwitterOAuth1Session) -> None:
        self._session = session

    def resource(
        self, url: OauthAuth1enticateUrl | Oauth1AuthorizeUrl
    ) -> OAuth1AuthenticateSessionResources | OAuth1AuthorizeSessionResources:
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
