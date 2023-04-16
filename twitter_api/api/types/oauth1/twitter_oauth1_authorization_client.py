from twitter_api.api.resources.oauth_authorize import OauthAuthorizeUrl
from twitter_api.api.types.oauth1.generate_authorization_url import (
    GenerateAuthorizationUrl,
)
from twitter_api.client.oauth_session.twitter_oauth1_session import TwitterOAuth1Session
from twitter_api.types.chainable import Chainable


class TwitterOAuth1AuthorizeClient(Chainable):
    def __init__(self, session: TwitterOAuth1Session) -> None:
        self._session = session

    def request(self, url: OauthAuthorizeUrl) -> GenerateAuthorizationUrl:
        return GenerateAuthorizationUrl(
            url,
            self._session,
        )
