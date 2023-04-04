from twitter_api.api.types.v2_cashtag import Cashtag
from twitter_api.types.extra_permissive_model import ExtraPermissiveModel


class RetweetEntitiesDescriptionCashtag(ExtraPermissiveModel):
    start: int
    end: int
    cashtag: Cashtag
