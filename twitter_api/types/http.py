from typing import TypedDict, TypeVar

from pydantic import BaseModel

Headers = TypeVar("Headers", bound=dict)
QuryParameters = TypeVar("QuryParameters", bound=dict)
RequestJsonBody = TypeVar("RequestJsonBody", bound=dict)
ResponseJsonBody = TypeVar("ResponseJsonBody", bound=dict)
ResponseModelBody = TypeVar("ResponseModelBody", bound=BaseModel)


def downcast_dict(typed_dict: TypedDict) -> dict:
    return typed_dict  # type: ignore
