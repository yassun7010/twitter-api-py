from twitter_api.types.extra_permissive_model import ExtraPermissiveModel

from .entity import Entity

DomainId = str


class Domain(ExtraPermissiveModel):
    id: DomainId
    name: str
    description: str
    entity: Entity
