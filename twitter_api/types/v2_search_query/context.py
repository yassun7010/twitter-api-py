from typing import Literal, Optional, overload

from twitter_api.types.v2_domain import DomainId
from twitter_api.types.v2_entity.entity_id import EntityId

from ._specific_keyword import SpecificKeyword
from .operator import Operator


class Context(SpecificKeyword, Operator[Operator]):
    @overload
    def __init__(
        self,
        context: str,
        *,
        domain_id: Literal[None] = None,
        entity_id: Literal[None] = None,
    ):
        ...

    @overload
    def __init__(
        self,
        context: Literal[None] = None,
        *,
        domain_id: DomainId,
        entity_id: EntityId,
    ):
        ...

    def __init__(
        self,
        context: Optional[str] = None,
        *,
        domain_id: Optional[DomainId] = None,
        entity_id: Optional[EntityId] = None,
    ):
        if context is None and domain_id is not None and entity_id is not None:
            context = f"{domain_id}.{entity_id}"
        elif context is None:
            raise ValueError(context)

        super().__init__(context, "context:")
