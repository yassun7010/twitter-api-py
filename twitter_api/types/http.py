from typing import Optional

from pydantic import BaseModel
from typing_extensions import TypeAlias, TypedDict, TypeVar, overload

Url: TypeAlias = str
Headers = TypeVar("Headers", bound=dict)
QuryParameters = TypeVar("QuryParameters", bound=dict)
RequestJsonBody = TypeVar("RequestJsonBody", bound=dict)
ResponseJsonBody = TypeVar("ResponseJsonBody", bound=dict)
ResponseModelBody = TypeVar("ResponseModelBody", bound=BaseModel)


@overload
def downcast_dict(typed_dict: TypedDict) -> dict:
    ...


@overload
def downcast_dict(typed_dict: Optional[TypedDict]) -> Optional[dict]:
    ...


def downcast_dict(typed_dict):
    return typed_dict
