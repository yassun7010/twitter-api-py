from twitter_api.client.oauth_session.resources.oauth_request_token import (
    OAuth1RequestTokenSessionResources,
    OauthRequestTokenUrl,
)
from twitter_api.client.oauth_session.twitter_oauth1_session import TwitterOAuth1Session
from twitter_api.types.chainable import Chainable


class TwitterOAuth1RequestTokenClient(Chainable):
    def __init__(self, session: TwitterOAuth1Session) -> None:
        self._session = session

    def resource(self, url: OauthRequestTokenUrl) -> OAuth1RequestTokenSessionResources:
        return OAuth1RequestTokenSessionResources(
            self._session,
        )
