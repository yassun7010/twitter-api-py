from twitter_api.types.extra_permissive_model import ExtraPermissiveModel


class RetweetPublicMetrics(ExtraPermissiveModel):
    followers_count: int
    following_count: int
    tweet_count: int
    listed_count: int
