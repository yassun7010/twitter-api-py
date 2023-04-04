import textwrap
from datetime import datetime
from typing import Optional

from twitter_api.types.extra_permissive_model import ExtraPermissiveModel

from ..v2_user.user_id import UserId
from .tweet_attachments import TweetAttachments
from .tweet_context_annotation import TweetContextAnnotation
from .tweet_edit_controls import TweetEditControls
from .tweet_entities import TweetEntities
from .tweet_geo import TweetGeo
from .tweet_id import TweetId
from .tweet_non_public_metrics import TweetNonPublicMetrics
from .tweet_organic_metrics import TweetOrganicMetrics
from .tweet_promoted_metrics import TweetPromotedMetrics
from .tweet_public_metrics import TweetPublicMetrics
from .tweet_referenced_tweet import TweetReferencedTweet
from .tweet_withheld import TweetWithheld


class Tweet(ExtraPermissiveModel):
    # flake8: noqa E501
    """
    ツイート情報。

    refer: https://developer.twitter.com/en/docs/twitter-api/data-dictionary/object-model/tweet
    """

    # Required
    id: TweetId
    text: str
    # 必須なはずだが、他の API では必須ではない。
    edit_history_tweet_ids: Optional[list[TweetId]] = None

    # Optional
    attachments: Optional[TweetAttachments] = None
    author_id: Optional[UserId] = None
    lang: Optional[str] = None
    context_annotations: Optional[list[TweetContextAnnotation]] = None
    conversation_id: Optional[str] = None
    created_at: Optional[datetime] = None
    edit_controls: Optional[TweetEditControls] = None
    entities: Optional[TweetEntities] = None
    geo: Optional[TweetGeo] = None
    in_reply_to_user_id: Optional[UserId] = None
    lang: Optional[str] = None
    non_public_metrics: Optional[TweetNonPublicMetrics] = None
    organic_metrics: Optional[TweetOrganicMetrics] = None
    possibly_sensitive: Optional[bool] = None
    promoted_metrics: Optional[TweetPromotedMetrics] = None
    public_metrics: Optional[TweetPublicMetrics] = None
    referenced_tweets: Optional[list[TweetReferencedTweet]] = None
    reply_settings: Optional[str] = None
    source: Optional[str] = None
    withheld: Optional[TweetWithheld] = None

    def __repr__(self):
        # 長すぎると可読性が落ちるので 最大 50 文字とする。
        text = textwrap.shorten(self.text, width=50, placeholder="...")
        return f'Tweet(id={self.id}, text="{text}")'
