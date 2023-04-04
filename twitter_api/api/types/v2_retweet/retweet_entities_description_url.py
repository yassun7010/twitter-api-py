from twitter_api.types.extra_permissive_model import ExtraPermissiveModel
from twitter_api.types.http import Url


class RetweetEntitiesDescriptionUrl(ExtraPermissiveModel):
    start: int
    end: int
    url: Url
    expanded_url: Url
    display_url: Url
