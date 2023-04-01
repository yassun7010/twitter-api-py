from twitter_api.types.extra_permissive_model import ExtraPermissiveModel

from ..domain import Domain
from ..entity import Entity


class TweetContextAnnotation(ExtraPermissiveModel):
    domain: Domain
    entity: Entity
