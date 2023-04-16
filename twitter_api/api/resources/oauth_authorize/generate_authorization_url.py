from twitter_api.api.resources.oauth_authorize import OauthAuthorizeUrl
from twitter_api.client.oauth_session.twitter_oauth1_session import TwitterOAuth1Session
from twitter_api.types.chainable import Chainable


class GenerateAuthorizationUrlOAuth1Session(Chainable):
    def __init__(
        self,
        url: OauthAuthorizeUrl,
        session: TwitterOAuth1Session,
    ):
        self._url = url
        self._session = session

    def generate_authorization_url(self):
        return self._session.generate_authorization_url()
