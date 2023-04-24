from typing import TypeAlias, TypeVar

from pydantic import BaseModel

Url: TypeAlias = str
Headers = TypeVar("Headers", bound=dict)
QuryParameters = TypeVar("QuryParameters", bound=dict)
RequestJsonBody = TypeVar("RequestJsonBody", bound=dict)
ResponseJsonBody = TypeVar("ResponseJsonBody", bound=dict)
ResponseModelBody = TypeVar("ResponseModelBody", bound=BaseModel)
