from typing import Optional

from twitter_api.types.extra_permissive_model import ExtraPermissiveModel

from .tweet_entities_annotation import TweetEntitiesAnnotation
from .tweet_entities_cashtag import TweetEntitiesCashtag
from .tweet_entities_hashtag import TweetEntitiesHashtag
from .tweet_entities_mention import TweetEntitiesMention
from .tweet_entities_url import TweetEntitiesUrl


class TweetEntities(ExtraPermissiveModel):
    annotations: Optional[list[TweetEntitiesAnnotation]] = None
    cashtags: Optional[list[TweetEntitiesCashtag]] = None
    hashtags: Optional[list[TweetEntitiesHashtag]] = None
    mentions: Optional[list[TweetEntitiesMention]] = None
    urls: Optional[list[TweetEntitiesUrl]] = None
