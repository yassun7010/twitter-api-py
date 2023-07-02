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
    _client_generator: Annotated[
        Callable[[AccessToken], TwitterApiGenericClient],
        Field(exclude=True),
    ]

    def generate_client(self) -> TwitterApiGenericClient:
        return self._client_generator(self.access_token)

    def model_dump_json(
        self,
        *,
        indent: int | None = None,
        by_alias: bool = False,
        exclude_unset: bool = False,
        exclude_defaults: bool = False,
        exclude_none: bool = False,
        round_trip: bool = False,
        warnings: bool = True,
    ) -> str:
        return super().model_dump_json(
            indent=indent,
            include=None,
            exclude=set("_client_generator"),
            by_alias=by_alias,
            exclude_unset=exclude_unset,
            exclude_defaults=exclude_defaults,
            exclude_none=exclude_none,
            round_trip=round_trip,
            warnings=warnings,
        )
