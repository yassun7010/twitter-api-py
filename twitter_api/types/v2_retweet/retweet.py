from datetime import datetime
from typing import Optional

from twitter_api.types.extra_permissive_model import ExtraPermissiveModel
from twitter_api.types.http import Url
from twitter_api.types.v2_retweet.retweet_entities import RetweetEntities
from twitter_api.types.v2_retweet.retweet_includes import RetweetIncludes
from twitter_api.types.v2_retweet.retweet_public_metrics import RetweetPublicMetrics
from twitter_api.types.v2_user.username import Username

from ..v2_tweet.tweet_id import TweetId
from .retweet_withheld import RetweetWithheld

DomainId = str


class Retweet(ExtraPermissiveModel):
    id: TweetId
    name: str
    username: Username
    created_at: Optional[datetime] = None
    protected: Optional[bool] = None
    withheld: Optional[RetweetWithheld] = None
    location: Optional[str] = None
    url: Optional[Url] = None
    description: Optional[str] = None
    verified: Optional[bool] = None
    entities: Optional[RetweetEntities] = None
    profile_image_url: Optional[Url] = None
    public_metrics: Optional[RetweetPublicMetrics] = None
    pinned_tweet_id: Optional[TweetId] = None
    includes: Optional[RetweetIncludes] = None
