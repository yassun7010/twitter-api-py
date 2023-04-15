from typing import Optional

from twitter_api.types.extra_permissive_model import ExtraPermissiveModel


class MediaPromotedMetrics(ExtraPermissiveModel):
    playback_0_count: Optional[int] = None
    playback_100_count: Optional[int] = None
    playback_25_count: Optional[int] = None
    playback_50_count: Optional[int] = None
    playback_75_count: Optional[int] = None
    view_count: Optional[int] = None
