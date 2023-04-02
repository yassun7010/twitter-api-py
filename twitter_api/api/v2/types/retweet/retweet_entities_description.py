from typing import Optional

from twitter_api.api.v2.types.retweet.retweet_entities_description_cashtag import (
    RetweetEntitiesDescriptionCashtag,
)
from twitter_api.api.v2.types.retweet.retweet_entities_description_hashtag import (
    RetweetEntitiesDescriptionHashtag,
)
from twitter_api.api.v2.types.retweet.retweet_entities_description_mention import (
    RetweetEntitiesDescriptionMention,
)
from twitter_api.api.v2.types.retweet.retweet_entities_description_url import (
    RetweetEntitiesDescriptionUrl,
)
from twitter_api.types.extra_permissive_model import ExtraPermissiveModel


class RetweetEntitiesDescription(ExtraPermissiveModel):
    urls: Optional[list[RetweetEntitiesDescriptionUrl]] = None
    hashtags: Optional[list[RetweetEntitiesDescriptionHashtag]] = None
    mentions: Optional[list[RetweetEntitiesDescriptionMention]] = None
    cashtags: Optional[list[RetweetEntitiesDescriptionCashtag]] = None