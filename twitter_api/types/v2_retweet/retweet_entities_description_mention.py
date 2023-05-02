from twitter_api.types.extra_permissive_model import ExtraPermissiveModel
from twitter_api.types.v2_user.username import Username


class RetweetEntitiesDescriptionMention(ExtraPermissiveModel):
    start: int
    end: int
    username: Username
