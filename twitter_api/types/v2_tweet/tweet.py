import textwrap
from datetime import datetime
from typing import Optional

from twitter_api.types.extra_permissive_model import ExtraPermissiveModel
from twitter_api.types.v2_tweet.tweet_entities_cashtag import TweetEntitiesCashtag
from twitter_api.types.v2_tweet.tweet_entities_hashtag import TweetEntitiesHashtag
from twitter_api.types.v2_tweet.tweet_entities_mention import TweetEntitiesMention
from twitter_api.types.v2_tweet.tweet_entities_url import TweetEntitiesUrl

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
    """
    ツイート情報。

    refer: https://developer.twitter.com/en/docs/twitter-api/data-dictionary/object-model/tweet
    """

    # Required
    id: TweetId
    text: str
    # 必須なはずだが、一部の API では必須ではないため、任意としている。
    #
    # このフィールドが存在する場合、少なくとも 1 つの要素が入ることになる。
    # そのため、 default_factory=list としても意図が曖昧になる。
    #
    # API によっては、クエリに `expansions=edit_history_tweet_ids` を与えた場合に出力されるものがある。
    #
    # refer: https://developer.twitter.com/en/docs/twitter-api/tweets/likes/api-reference/get-users-id-liked_tweets
    #
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

    def __repr__(self) -> str:
        # 長すぎると可読性が落ちるので 最大 50 文字とする。
        text = textwrap.shorten(self.text, width=50, placeholder="...")
        return f'Tweet(id={self.id}, text="{text}")'

    @property
    def entities_urls(self) -> list[TweetEntitiesUrl]:
        """
        ツイート文の中にある URL 情報のリストを返す。
        """
        if self.entities is None or self.entities.urls is None:
            return []
        else:
            return self.entities.urls

    @property
    def entities_mentions(self) -> list[TweetEntitiesMention]:
        """
        ツイート文の中にあるメンション情報のリストを返す。
        """
        if self.entities is None or self.entities.mentions is None:
            return []
        else:
            return self.entities.mentions

    @property
    def public_metrics_like_count(self) -> Optional[int]:
        """
        「いいね」の数を取得する。
        """
        if self.public_metrics is None:
            return None
        else:
            return self.public_metrics.like_count

    @property
    def public_metrics_retweet_count(self) -> Optional[int]:
        """
        リツイートされた数を取得する。
        """
        if self.public_metrics is None:
            return None
        else:
            return self.public_metrics.retweet_count

    @property
    def retweeted_tweet_id(self) -> Optional[TweetId]:
        """
        リツイート元の TweetID を取得する。
        """
        if self.referenced_tweets is None:
            return None

        for tweet in self.referenced_tweets:
            if tweet.type == "retweeted":
                return tweet.id

        return None

    @property
    def is_retweet(self) -> Optional[bool]:
        """
        リツイートかどうか。

        None の場合、判断できる情報がない。
        """
        if self.referenced_tweets is None:
            return None

        for tweet in self.referenced_tweets:
            if tweet.type == "retweeted":
                return True

        return False

    @property
    def quoted_tweet_id(self) -> Optional[TweetId]:
        """
        引用元の TweetID を取得する。
        """
        if self.referenced_tweets is None:
            return None

        for tweet in self.referenced_tweets:
            if tweet.type == "quoted":
                return tweet.id

        return None

    @property
    def is_quote(self) -> Optional[bool]:
        """
        引用ツイートであるかどうか。

        None の場合、判断できる情報がない。
        """

        if self.referenced_tweets is None:
            return None

        for tweet in self.referenced_tweets:
            if tweet.type == "quoted":
                return True

        return False

    @property
    def replied_tweet_id(self) -> Optional[TweetId]:
        """
        リプライ元の TweetId を取得する。
        """
        if self.referenced_tweets is None:
            return None

        for tweet in self.referenced_tweets:
            if tweet.type == "replied_to":
                return tweet.id

        return None

    @property
    def is_reply(self) -> Optional[bool]:
        """
        リプライツイートであるかどうか。

        None の場合、判断できる情報がない。
        """
        if self.referenced_tweets is None:
            return None

        for tweet in self.referenced_tweets:
            if tweet.type == "replied_to":
                return True

        return False

    @property
    def entities_hashtags(self) -> Optional[list[TweetEntitiesHashtag]]:
        """
        ハッシュタグ情報。
        """
        if self.entities is None or self.entities.hashtags is None:
            return None

        return self.entities.hashtags

    @property
    def has_hashtags(self) -> Optional[bool]:
        """
        ハッシュタグがついているかどうか。

        None の場合、判断できる情報がない。
        """
        if self.entities is None or self.entities.hashtags is None:
            return None

        return len(self.entities.hashtags) != 0

    @property
    def entities_cashtags(self) -> Optional[list[TweetEntitiesCashtag]]:
        """
        キャッシュタグ情報。
        """
        if self.entities is None or self.entities.cashtags is None:
            return None

        return self.entities.cashtags

    @property
    def has_cashtags(self) -> Optional[bool]:
        """
        キャッシュタグがついているかどうか。

        None の場合、判断できる情報がない。
        """
        if self.entities is None or self.entities.cashtags is None:
            return None

        return len(self.entities.cashtags) != 0
