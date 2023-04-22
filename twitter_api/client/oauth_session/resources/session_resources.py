from twitter_api.client.oauth_session.twitter_oauth1_session import TwitterOAuth1Session
from twitter_api.client.oauth_session.twitter_oauth2_session import TwitterOAuth2Session


class OAuth1SessionResources:
    def __init__(self, session: TwitterOAuth1Session) -> None:
        self._session = session


class OAuth2SessionResources:
    def __init__(self, session: TwitterOAuth2Session) -> None:
        self._session = session
