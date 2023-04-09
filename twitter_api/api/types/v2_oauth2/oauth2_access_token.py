from typing_extensions import Literal

from twitter_api.api.types.v2_scope import Scope
from twitter_api.types.chainable import Chainable
from twitter_api.types.extra_permissive_model import ExtraPermissiveModel
from twitter_api.types.oauth import AccessToken


class OAuth2AccessToken(Chainable, ExtraPermissiveModel):
    token_type: Literal["bearer"]
    expires_in: int
    expires_at: int
    access_token: AccessToken
    scope: list[Scope]
