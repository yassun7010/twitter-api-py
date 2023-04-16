from twitter_api.api.resources.oauth_authorize import OauthAuthorizeUrl
from twitter_api.api.resources.oauth_authorize.generate_authorization_url import (
    GenerateAuthorizationUrlOAuth1Session,
)
from twitter_api.client.oauth_session.twitter_oauth1_session import TwitterOAuth1Session
from twitter_api.types.chainable import Chainable


class TwitterOAuth1AuthorizeClient(Chainable):
    def __init__(self, session: TwitterOAuth1Session) -> None:
        self._session = session

    def request(self, url: OauthAuthorizeUrl) -> GenerateAuthorizationUrlOAuth1Session:
        return GenerateAuthorizationUrlOAuth1Session(
            url,
            self._session,
        )
