from typing_extensions import Literal

from twitter_api.api.types.v2_scope import Scope
from twitter_api.api.types.v2_user.user_id import UserId
from twitter_api.types.chainable import Chainable
from twitter_api.types.extra_permissive_model import ExtraPermissiveModel
from twitter_api.types.oauth import AccessSecret, AccessToken


class OAuth1AccessToken(Chainable, ExtraPermissiveModel):
    oauth_token: AccessToken
    oauth_token_secret: AccessSecret
    user_id: UserId
    screen_name: str
