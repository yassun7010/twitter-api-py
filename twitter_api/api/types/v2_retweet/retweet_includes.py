from pydantic import Field

from twitter_api.api.types.v2_tweet.tweet import Tweet
from twitter_api.types.extra_permissive_model import ExtraPermissiveModel


class RetweetIncludes(ExtraPermissiveModel):
    tweets: list[Tweet] = Field(default_factory=list)
