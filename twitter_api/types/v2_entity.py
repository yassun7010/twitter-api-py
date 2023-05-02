from typing import Optional, TypeAlias

from twitter_api.types.extra_permissive_model import ExtraPermissiveModel

EntityId: TypeAlias = str


class Entity(ExtraPermissiveModel):
    id: EntityId
    name: str
    description: Optional[str] = None
