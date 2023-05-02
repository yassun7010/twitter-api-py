from pydantic import Field

from twitter_api.types.extra_permissive_model import ExtraPermissiveModel
from twitter_api.types.v2_tweet.tweet import Tweet


class RetweetIncludes(ExtraPermissiveModel):
    tweets: list[Tweet] = Field(default_factory=list)
