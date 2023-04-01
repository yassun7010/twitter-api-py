from typing import Optional

from twitter_api.types.extra_permissive_model import ExtraPermissiveModel


class TweetNonPublicMetrics(ExtraPermissiveModel):
    impression_count: Optional[int] = None
    url_link_clicks: Optional[int] = None
    user_profile_clicks: Optional[int] = None
