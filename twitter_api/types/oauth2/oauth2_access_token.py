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

from typing_extensions import Literal

from twitter_api.types._generic_client import TwitterApiGenericClient
from twitter_api.types.extra_permissive_model import ExtraPermissiveModel
from twitter_api.types.oauth import AccessToken
from twitter_api.types.v2_scope import Scope

if TYPE_CHECKING:
    IntStr = Union[int, str]
    AbstractSetIntStr = AbstractSet[IntStr]
    MappingIntStrAny = Mapping[IntStr, Any]


class OAuth2AccessToken(Generic[TwitterApiGenericClient], ExtraPermissiveModel):
    token_type: Literal["bearer"]
    expires_in: int
    expires_at: int
    access_token: AccessToken
    scope: list[Scope]
    _client_generator: Callable[[AccessToken], TwitterApiGenericClient]

    def generate_client(self) -> TwitterApiGenericClient:
        return self._client_generator(self.access_token)

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
