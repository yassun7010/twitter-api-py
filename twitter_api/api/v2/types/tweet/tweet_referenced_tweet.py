from typing import Optional

from twitter_api.types.extra_permissive_model import ExtraPermissiveModel

from .tweet_id import TweetId


class TweetReferencedTweet(ExtraPermissiveModel):
    type: Optional[str] = None
    id: Optional[TweetId] = None
