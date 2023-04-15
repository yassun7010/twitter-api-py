from typing import Optional

from twitter_api.types.extra_permissive_model import ExtraPermissiveModel

from .v2_entity import Entity

DomainId = str


class Domain(ExtraPermissiveModel):
    id: DomainId
    name: str
    description: Optional[str] = None
    entity: Optional[Entity] = None
