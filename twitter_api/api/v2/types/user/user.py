from datetime import datetime
from typing import Any, Optional

from twitter_api.types.extra_permissive_model import ExtraPermissiveModel

from ..tweet.tweet_id import TweetId
from .user_id import UserId


class User(ExtraPermissiveModel):
    id: UserId
    name: str
    username: str
    created_at: datetime
    description: Optional[str] = None
    entities: Optional[dict[str, Any]] = None
    location: Optional[str] = None
    pinned_tweet_id: Optional[TweetId] = None
    profile_image_url: Optional[str] = None
    protected: Optional[bool] = None
    public_metrics: Optional[dict[str, Any]] = None
    url: Optional[str] = None
    verified: Optional[bool] = None
    withheld: Optional[dict[str, Any]] = None
