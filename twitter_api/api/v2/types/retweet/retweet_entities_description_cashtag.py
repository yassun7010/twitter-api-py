from twitter_api.api.v2.types.cashtag import Cashtag
from twitter_api.types.extra_permissive_model import ExtraPermissiveModel


class RetweetEntitiesDescriptionCashtag(ExtraPermissiveModel):
    start: int
    end: int
    cashtag: Cashtag
