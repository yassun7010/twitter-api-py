from twitter_api.api.v2.types.username import Username
from twitter_api.types.extra_permissive_model import ExtraPermissiveModel


class RetweetEntitiesDescriptionMention(ExtraPermissiveModel):
    start: int
    end: int
    username: Username
