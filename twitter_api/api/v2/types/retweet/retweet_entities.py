from twitter_api.api.v2.types.retweet.retweet_entities_description import (
    RetweetEntitiesDescription,
)
from twitter_api.api.v2.types.retweet.retweet_entities_url import RetweetEntitiesUrl
from twitter_api.types.extra_permissive_model import ExtraPermissiveModel


class RetweetEntities(ExtraPermissiveModel):
    url: list[RetweetEntitiesUrl]
    description: list[RetweetEntitiesDescription]
