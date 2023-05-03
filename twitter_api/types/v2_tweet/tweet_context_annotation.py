from twitter_api.types.extra_permissive_model import ExtraPermissiveModel
from twitter_api.types.v2_domain import Domain
from twitter_api.types.v2_entity.entity import Entity


class TweetContextAnnotation(ExtraPermissiveModel):
    domain: Domain
    entity: Entity
