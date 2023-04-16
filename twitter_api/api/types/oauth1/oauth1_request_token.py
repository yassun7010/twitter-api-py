from twitter_api.client.oauth_session.twitter_oauth1_session import TwitterOAuth1Session
from twitter_api.types.chainable import Chainable


class OAuth1RequestToken(Chainable):
    def __init__(
        self,
        session: TwitterOAuth1Session,
    ) -> None:
        self._session = session
