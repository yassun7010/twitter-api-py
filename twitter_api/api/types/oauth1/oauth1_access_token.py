from typing_extensions import Literal

from twitter_api.api.types.v2_scope import Scope
from twitter_api.api.types.v2_user.user_id import UserId
from twitter_api.client.oauth_session.twitter_oauth1_session import TwitterOAuth1Session
from twitter_api.types.chainable import Chainable
from twitter_api.types.extra_permissive_model import ExtraPermissiveModel
from twitter_api.types.oauth import AccessSecret, AccessToken


class OAuth1AccessToken(Chainable, ExtraPermissiveModel):
    oauth_token: AccessToken
    oauth_token_secret: AccessSecret
    user_id: UserId
    screen_name: str
    _session: TwitterOAuth1Session

    def generate_client(self):
        return self._session.generate_client(self.oauth_token, self.oauth_token_secret)
