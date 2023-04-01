from typing import TypeVar

from pydantic import BaseModel

Headers = TypeVar("Headers", bound=dict)
QuryParameters = TypeVar("QuryParameters", bound=dict)
RequestJsonBody = TypeVar("RequestJsonBody", bound=dict)
RequestModelBody = TypeVar("RequestModelBody", bound=BaseModel)
ResponseJsonBody = TypeVar("ResponseJsonBody", bound=dict)
ResponseModelBody = TypeVar("ResponseModelBody", bound=BaseModel)
ResponseBody = TypeVar("ResponseBody", str, BaseModel)
