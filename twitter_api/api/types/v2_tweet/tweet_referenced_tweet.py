from typing import Literal

from twitter_api.types.extra_permissive_model import ExtraPermissiveModel

from .tweet_id import TweetId


class TweetReferencedTweet(ExtraPermissiveModel):
    type: Literal["retweeted", "quoted", "replied_to"]
    id: TweetId
