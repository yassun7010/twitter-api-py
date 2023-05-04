from twitter_api.types.extra_permissive_model import ExtraPermissiveModel
from twitter_api.types.v2_cashtag import Cashtag


class RetweetEntitiesDescriptionCashtag(ExtraPermissiveModel):
    start: int
    end: int
    cashtag: Cashtag
