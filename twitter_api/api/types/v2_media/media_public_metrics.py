from typing import Optional

from twitter_api.types.extra_permissive_model import ExtraPermissiveModel


class MediaPublicMetrics(ExtraPermissiveModel):
    view_count: Optional[int] = None
