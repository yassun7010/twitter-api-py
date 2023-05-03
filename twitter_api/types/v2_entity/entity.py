from typing import Optional

from twitter_api.types.extra_permissive_model import ExtraPermissiveModel

from .entity_id import EntityId
from .entity_name import EntityName


class Entity(ExtraPermissiveModel):
    id: EntityId
    name: EntityName
    description: Optional[str] = None
