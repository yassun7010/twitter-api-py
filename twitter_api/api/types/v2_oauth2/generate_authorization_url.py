from authlib.integrations.requests_client.oauth2_session import OAuth2Session

from twitter_api.api.resources.oauth2_authorize import Oauth2AuthorizeUrl
from twitter_api.api.types.v2_oauth2.oauth2_authorization import OAuth2Authorization
from twitter_api.types.chainable import Chainable
from twitter_api.utils.oauth import generate_code_verifier


class GenerateAuthorizationUrl(Chainable):
    def __init__(self, url: Oauth2AuthorizeUrl, session: OAuth2Session):
        self._url = url
        self._session = session

    def generate_authorization_url(self):
        code_verifier = generate_code_verifier()

        authorization_url, state = self._session.create_authorization_url(
            self._url, code_verifier=code_verifier
        )

        return OAuth2Authorization(
            authorization_url=authorization_url,
            state=state,
            code_verifier=code_verifier,
            _session=self._session,
        )
