from twitter_api.types.extra_permissive_model import ExtraPermissiveModel
from twitter_api.types.http import Url


class MediaVariants(ExtraPermissiveModel):
    bit_rate: int
    content_type: str
    url: Url
