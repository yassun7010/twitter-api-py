from twitter_api.client.oauth_session.resources.oauth_authenticate import (
    OAuthAuthenticateSessionResources,
    OauthAuthenticateUrl,
)
from twitter_api.client.oauth_session.resources.oauth_authorize import (
    OAuthAuthorizeSessionResources,
    OauthAuthorizeUrl,
)
from twitter_api.client.oauth_session.twitter_oauth1_session import TwitterOAuth1Session
from twitter_api.error import NeverError
from twitter_api.types.chainable import Chainable


class TwitterOAuth1AuthorizeClient(Chainable):
    def __init__(self, session: TwitterOAuth1Session) -> None:
        self._session = session

    def resource(
        self, url: OauthAuthenticateUrl | OauthAuthorizeUrl
    ) -> OAuthAuthenticateSessionResources | OAuthAuthorizeSessionResources:
        if url == "https://api.twitter.com/oauth/authenticate":
            return OAuthAuthenticateSessionResources(
                self._session,
            )
        elif url == "https://api.twitter.com/oauth/authorize":
            return OAuthAuthorizeSessionResources(
                self._session,
            )
        else:
            raise NeverError(url)
