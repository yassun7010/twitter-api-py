from typing import Optional, TypeAlias

from twitter_api.types.extra_permissive_model import ExtraPermissiveModel
from twitter_api.types.v2_entity.entity import Entity

DomainId: TypeAlias = str


class Domain(ExtraPermissiveModel):
    id: DomainId
    name: str
    description: Optional[str] = None
    entity: Optional[Entity] = None
