from twitter_api.types.extra_permissive_model import ExtraPermissiveModel
from twitter_api.types.http import Url


class RetweetEntitiesUrlUrl(ExtraPermissiveModel):
    start: int
    end: int
    url: Url
    expanded_url: Url
    display_url: Url


class RetweetEntitiesUrl(ExtraPermissiveModel):
    urls: list[RetweetEntitiesUrlUrl]
