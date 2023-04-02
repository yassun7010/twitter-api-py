from twitter_api.api.v2.types.tweet.tweet import Tweet
from twitter_api.types.extra_permissive_model import ExtraPermissiveModel


class RetweetIncludes(ExtraPermissiveModel):
    tweets: list[Tweet]
