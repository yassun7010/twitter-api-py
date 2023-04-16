from twitter_api.api.resources.oauth_authenticate import OauthAuthenticateUrl
from twitter_api.api.resources.oauth_authorize import OauthAuthorizeUrl
from twitter_api.api.types.oauth1.oauth1_generate_authorization_url import (
    OAuth1GenerateAuthorizationUrlSession,
)
from twitter_api.api.types.oauth1.oauth1_request_url import OAuth1RequestUrl
from twitter_api.client.oauth_session.twitter_oauth1_session import TwitterOAuth1Session
from twitter_api.types.chainable import Chainable


class TwitterOAuth1AuthorizeClient(Chainable):
    def __init__(self, session: TwitterOAuth1Session) -> None:
        self._session = session

    def request(self, url: OAuth1RequestUrl) -> OAuth1GenerateAuthorizationUrlSession:
        return OAuth1GenerateAuthorizationUrlSession(
            url,
            self._session,
        )
