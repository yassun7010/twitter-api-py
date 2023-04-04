from typing import Optional

from twitter_api.types.extra_permissive_model import ExtraPermissiveModel

EntityId = str


class Entity(ExtraPermissiveModel):
    id: EntityId
    name: str
    description: Optional[str] = None
