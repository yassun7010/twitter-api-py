from typing import Optional

from twitter_api.types.extra_permissive_model import ExtraPermissiveModel


class TweetPublicMetrics(ExtraPermissiveModel):
    impression_count: Optional[int] = None
    url_link_clicks: Optional[int] = None
    user_profile_clicks: Optional[int] = None
    like_count: Optional[int] = None
    quote_count: Optional[int] = None
    reply_count: Optional[int] = None
    retweet_count: Optional[int] = None
