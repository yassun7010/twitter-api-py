from twitter_api.types.extra_permissive_model import ExtraPermissiveModel
from twitter_api.types.v2_retweet.retweet_entities_description import (
    RetweetEntitiesDescription,
)
from twitter_api.types.v2_retweet.retweet_entities_url import RetweetEntitiesUrl


class RetweetEntities(ExtraPermissiveModel):
    url: list[RetweetEntitiesUrl]
    description: list[RetweetEntitiesDescription]
