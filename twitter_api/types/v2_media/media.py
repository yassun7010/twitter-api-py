from typing import Literal, Optional

from twitter_api.types.extra_permissive_model import ExtraPermissiveModel
from twitter_api.types.http import Url
from twitter_api.types.v2_media.media_key import MediaKey
from twitter_api.types.v2_media.media_non_public_metrics import MediaNonPublicMetrics
from twitter_api.types.v2_media.media_organic_metrics import MediaOrganicMetrics
from twitter_api.types.v2_media.media_promoted_metrics import MediaPromotedMetrics
from twitter_api.types.v2_media.media_public_metrics import MediaPublicMetrics
from twitter_api.types.v2_media.media_variants import MediaVariants


class Media(ExtraPermissiveModel):
    """
    メディアの情報。

    refer: https://developer.twitter.com/en/docs/twitter-api/data-dictionary/object-model/media
    """

    media_key: MediaKey
    type: Literal["animated_gif", "photo", "video"]
    url: Optional[Url] = None
    preview_image_url: Optional[Url] = None
    alt_text: Optional[str] = None
    duration_ms: Optional[int] = None
    height: Optional[int] = None
    width: Optional[int] = None
    public_metrics: Optional[MediaPublicMetrics] = None
    non_public_metrics: Optional[MediaNonPublicMetrics] = None
    organic_metrics: Optional[MediaOrganicMetrics] = None
    promoted_metrics: Optional[MediaPromotedMetrics] = None
    variants: Optional[MediaVariants] = None
