from twitter_api.types.extra_permissive_model import ExtraPermissiveModel

from ..v2_domain import Domain
from ..v2_entity import Entity


class TweetContextAnnotation(ExtraPermissiveModel):
    domain: Domain
    entity: Entity
