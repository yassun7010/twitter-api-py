from typing import (
    TYPE_CHECKING,
    AbstractSet,
    Annotated,
    Any,
    Callable,
    Generic,
    Mapping,
    Union,
)

from pydantic import Field

from twitter_api.types._generic_client import TwitterApiGenericClient
from twitter_api.types.extra_permissive_model import ExtraPermissiveModel
from twitter_api.types.oauth import AccessSecret, AccessToken
from twitter_api.types.v2_user.user_id import UserId
from twitter_api.types.v2_user.username import Username

if TYPE_CHECKING:
    IntStr = Union[int, str]
    AbstractSetIntStr = AbstractSet[IntStr]
    MappingIntStrAny = Mapping[IntStr, Any]


class OAuth1AccessToken(Generic[TwitterApiGenericClient], ExtraPermissiveModel):
    oauth_token: AccessToken
    oauth_token_secret: AccessSecret
    user_id: UserId
    screen_name: Username
    _client_generator: Annotated[
        Callable[[AccessToken, AccessSecret], TwitterApiGenericClient],
        Field(exclude=True),
    ]

    def generate_client(self) -> TwitterApiGenericClient:
        return self._client_generator(self.oauth_token, self.oauth_token_secret)
