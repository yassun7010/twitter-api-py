from typing import Generic

from twitter_api.client.oauth_session.twitter_oauth1_session import TwitterOAuth1Session
from twitter_api.types.extra_permissive_model import ExtraPermissiveModel
from twitter_api.types.generic_client import TwitterApiGenericClient
from twitter_api.types.oauth import AccessSecret, AccessToken
from twitter_api.types.v2_user.user_id import UserId
from twitter_api.types.v2_user.username import Username


class OAuth1AccessToken(Generic[TwitterApiGenericClient], ExtraPermissiveModel):
    oauth_token: AccessToken
    oauth_token_secret: AccessSecret
    user_id: UserId
    screen_name: Username
    _session: TwitterOAuth1Session[TwitterApiGenericClient]

    def generate_client(self) -> TwitterApiGenericClient:
        return self._session.generate_client(self.oauth_token, self.oauth_token_secret)
