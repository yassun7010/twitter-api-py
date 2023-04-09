from twitter_api.api.resources.oauth2_authorize import Oauth2AuthorizeUrl
from twitter_api.client.sessions.twitter_oauth2_session import TwitterOAuth2Session
from twitter_api.types.chainable import Chainable


class GenerateAuthorizationUrl(Chainable):
    def __init__(
        self,
        url: Oauth2AuthorizeUrl,
        session: TwitterOAuth2Session,
    ):
        self._url = url
        self._session = session

    def generate_authorization_url(self):
        return self._session.generate_authorization_url()
