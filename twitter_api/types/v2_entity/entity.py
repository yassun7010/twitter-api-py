from typing import Optional

from twitter_api.types.extra_permissive_model import ExtraPermissiveModel

from .entity_id import EntityId


class Entity(ExtraPermissiveModel):
    id: EntityId
    name: str
    description: Optional[str] = None
