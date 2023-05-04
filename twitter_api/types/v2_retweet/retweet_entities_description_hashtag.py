from twitter_api.types.extra_permissive_model import ExtraPermissiveModel
from twitter_api.types.v2_hashtag import Hashtag


class RetweetEntitiesDescriptionHashtag(ExtraPermissiveModel):
    start: int
    end: int
    hashtag: Hashtag
