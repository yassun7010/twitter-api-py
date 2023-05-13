from typing import (
    TYPE_CHECKING,
    AbstractSet,
    Any,
    Callable,
    Generic,
    Mapping,
    Optional,
    Union,
)

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
    _client_generator: Callable[[AccessToken, AccessSecret], TwitterApiGenericClient]

    def generate_client(self) -> TwitterApiGenericClient:
        return self._client_generator(self.oauth_token, self.oauth_token_secret)

    def json(
        self,
        *,
        include: Optional[Union["AbstractSetIntStr", "MappingIntStrAny"]] = None,
        exclude: Optional[Union["AbstractSetIntStr", "MappingIntStrAny"]] = {
            "_client_generator"
        },
        by_alias: bool = False,
        skip_defaults: Optional[bool] = None,
        exclude_unset: bool = True,
        exclude_defaults: bool = False,
        exclude_none: bool = True,
        encoder: Optional[Callable[[Any], Any]] = None,
        models_as_dict: bool = True,
        ensure_ascii=False,
        **dumps_kwargs: Any,
    ) -> str:
        return super().json(
            include=include,
            exclude=exclude,
            by_alias=by_alias,
            skip_defaults=skip_defaults,
            exclude_unset=exclude_unset,
            exclude_defaults=exclude_defaults,
            exclude_none=exclude_none,
            encoder=encoder,
            models_as_dict=models_as_dict,
            ensure_ascii=ensure_ascii,
            **dumps_kwargs,
        )
