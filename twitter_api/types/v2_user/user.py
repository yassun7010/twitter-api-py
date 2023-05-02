from datetime import datetime
from typing import Any, Optional

from twitter_api.types.extra_permissive_model import ExtraPermissiveModel
from twitter_api.types.http import Url
from twitter_api.types.v2_user.user_verified_type import UserVerifiedType
from twitter_api.types.v2_user.username import Username

from ..v2_tweet.tweet_id import TweetId
from .user_id import UserId


class User(ExtraPermissiveModel):
    id: UserId
    name: str
    username: Username
    created_at: Optional[datetime] = None
    description: Optional[str] = None
    entities: Optional[dict[str, Any]] = None
    location: Optional[str] = None
    pinned_tweet_id: Optional[TweetId] = None
    profile_image_url: Optional[Url] = None
    protected: Optional[bool] = None
    public_metrics: Optional[dict[str, Any]] = None
    url: Optional[Url] = None
    verified: Optional[bool] = None
    verified_type: Optional[UserVerifiedType] = None
    withheld: Optional[dict[str, Any]] = None
