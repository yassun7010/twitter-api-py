from twitter_api.types.extra_permissive_model import ExtraPermissiveModel


class RetweetEntitiesDescriptionHashtag(ExtraPermissiveModel):
    start: int
    end: int
    hashtag: str
