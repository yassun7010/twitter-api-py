from abc import ABCMeta, abstractmethod
from typing import Any, Callable, Literal, Type, Union, overload

from twitter_api.types.v2_cashtag import Cashtag
from twitter_api.types.v2_dm_conversation.dm_conversation_id import DmConversationId
from twitter_api.types.v2_domain import DomainId
from twitter_api.types.v2_entity.entity_id import EntityId
from twitter_api.types.v2_entity.entity_name import EntityName
from twitter_api.types.v2_hashtag import Hashtag
from twitter_api.types.v2_language import Language
from twitter_api.types.v2_list.list_id import ListId
from twitter_api.types.v2_place.place_country_code import PlaceCountryCode
from twitter_api.types.v2_place.place_id import PlaceId
from twitter_api.types.v2_place.place_name import PlaceName
from twitter_api.types.v2_search_query.operators.bounding_box_operator import (
    BoundingBoxOperator,
)
from twitter_api.types.v2_search_query.operators.has_cashtags_operator import (
    HasCashtagsOperator,
)
from twitter_api.types.v2_search_query.operators.has_geo_operator import HasGeoOperator
from twitter_api.types.v2_search_query.operators.has_hashtags_operator import (
    HasHashtagsOperator,
)
from twitter_api.types.v2_search_query.operators.has_images_operator import (
    HasImagesOperator,
)
from twitter_api.types.v2_search_query.operators.has_links_operator import (
    HasLinksOperator,
)
from twitter_api.types.v2_search_query.operators.has_media_operator import (
    HasMediaOperator,
)
from twitter_api.types.v2_search_query.operators.has_mentions_operator import (
    HasMentionsOperator,
)
from twitter_api.types.v2_search_query.operators.has_video_link_operator import (
    HasVideoLinkOperator,
)
from twitter_api.types.v2_search_query.operators.is_nullcast_operator import (
    IsNullcastOperator,
)
from twitter_api.types.v2_search_query.operators.is_quote_operator import (
    IsQuoteOperator,
)
from twitter_api.types.v2_search_query.operators.is_reply_operator import (
    IsReplyOperator,
)
from twitter_api.types.v2_search_query.operators.is_retweet_operator import (
    IsRetweetOperator,
)
from twitter_api.types.v2_search_query.operators.is_verified_operator import (
    IsVerifiedOperator,
)
from twitter_api.types.v2_search_query.operators.lang_operator import LangOperator
from twitter_api.types.v2_search_query.operators.place_country_operator import (
    PlaceCountryOperator,
)
from twitter_api.types.v2_search_query.operators.place_operator import PlaceOperator
from twitter_api.types.v2_search_query.operators.point_radius_operator import (
    PointRadiusOperator,
)
from twitter_api.types.v2_tweet.tweet_context_annotation import TweetContextAnnotation
from twitter_api.types.v2_tweet.tweet_id import TweetId
from twitter_api.types.v2_user.user_id import UserId
from twitter_api.types.v2_user.username import Username

from .operators.cashtag_operator import CashtagOperator
from .operators.context_operator import ContextOperator
from .operators.conversation_id_operator import ConversationIdOperator
from .operators.entity_operator import EntityOperator
from .operators.from_user_operator import FromUserOperator
from .operators.group_operator import GroupOperator, grouping
from .operators.hashtag_operator import HashtagOperator
from .operators.in_reply_to_tweet_id_operator import InReplyToTweetIdOperator
from .operators.keyword_operator import KeywordOperator
from .operators.list_operator import ListOperator
from .operators.mention_operator import MentionOperator
from .operators.operator import CorrectOperator, Operator
from .operators.quotes_of_tweet_id_operator import QuotesOfTweetIdOperator
from .operators.retweet_of_operator import RetweetOfOperator
from .operators.retweets_of_tweet_id_operator import RetweetsOfTweetIdOperator
from .operators.to_user_operator import ToUserOperator
from .operators.url_operator import UrlOperator


class SearchQuery:
    """
    検索クエリの作成をエディタの支援を受けながら行うためのクラス。

    SearchQuery.build を用いて作成する。

    refer: https://developer.twitter.com/en/docs/twitter-api/tweets/search/integrate/build-a-query
    """

    def __init__(self, *query: Operator) -> None:
        self._query = query

    def __str__(self) -> str:
        return " ".join(map(grouping, self._query))

    @classmethod
    def build(
        cls,
        building: Callable[
            [Type["_SearchQueryBuilder"]],
            CorrectOperator,
        ],
    ):
        """
        検索クエリを組み立てる。

        静的解析でエラーを出さずにクエリを組み立てるには、下記のルールに従う。

        - クエリの先頭、またはグループの先頭は Standalone Operator を置く必要がある。
        - Conjunction Required Operator は成立するクエリの右側に & 結合していく。
        - AND 演算（ & 結合）は、左側はクエリとして成立するものである必要がある。
        - OR 演算（ | 結合） はその左右がクエリとして成立するものである必要がある。
        - NOT 演算（ ~ ）はクエリの先頭、またはグループの先頭に設置できない。
        - グループへの否定、二重否定はできない。

        >>> from .search_query import SearchQuery
        >>> query = SearchQuery.build(
        ...     lambda q: (
        ...         q.group(
        ...             q.hashtag("#Twitter") | q.hashtag("Xcorp"),
        ...         )
        ...         & q.mention("@elonmusk")
        ...         & ~q.mention("SpaceX")
        ...         & q.is_retweet()
        ...     )
        ... )
        >>> str(query)
        '(#Twitter OR #Xcorp) @elonmusk -@SpaceX is:retweet'
        """

        return SearchQuery(building(_SearchQueryBuilder))


class _SearchQueryBuilder(metaclass=ABCMeta):
    @abstractmethod
    def __init__(self) -> None:
        ...

    @classmethod
    def keyword(cls, keyword: str) -> KeywordOperator:
        """
        キーワードによる絞り込み。

        空白が含まれる場合、ダブルクォーテーションで囲まれる。
        """
        return KeywordOperator(keyword)

    @classmethod
    def mention(cls, username: Username) -> MentionOperator:
        """
        メンションによる絞り込み。

        先頭に @ がない場合、 @ をつけて処理される。
        """
        return MentionOperator(username)

    @classmethod
    def hashtag(cls, hashtag: Hashtag) -> HashtagOperator:
        """
        ハッシュタグによる絞り込み。

        先頭に # がない場合、 # をつけて処理される。
        """
        return HashtagOperator(hashtag)

    @classmethod
    def cashtag(cls, cashtag: Cashtag) -> CashtagOperator:
        """
        キャッシュタグによる絞り込み。

        先頭に $ がない場合、 $ をつけて処理される。
        """
        return CashtagOperator(cashtag)

    @classmethod
    def group(cls, operator: CorrectOperator, *operators: Operator) -> GroupOperator:
        """
        括弧で囲みたい対象を指定する。

        要素数が 1 つの場合は括弧をつけない。
        """
        return GroupOperator(operator, *operators)

    @classmethod
    def from_user(cls, user: Union[UserId, Username]) -> FromUserOperator:
        """
        どのユーザからツイートされたかで絞り込む。
        """
        return FromUserOperator(user)

    @classmethod
    def to_user(cls, user: Union[UserId, Username]) -> ToUserOperator:
        """
        どのユーザへツイートしたかで絞り込む。
        """
        return ToUserOperator(user)

    @classmethod
    def url(cls, url: str) -> UrlOperator:
        """
        ツイートに含まれる URL で絞り込む。
        """
        return UrlOperator(url)

    @classmethod
    def retweet_of(cls, user: Union[UserId, Username]) -> RetweetOfOperator:
        """
        どのユーザへのリツイートかで絞り込む。
        """
        return RetweetOfOperator(user)

    @classmethod
    def in_reply_to_tweet_id(cls, id: TweetId) -> InReplyToTweetIdOperator:
        """
        どのツイートへのリプライかで絞り込む。
        """
        return InReplyToTweetIdOperator(id)

    @classmethod
    def retweets_of_tweet_id(cls, id: TweetId) -> RetweetsOfTweetIdOperator:
        """
        どのツイートへのリツイートかで絞り込む。
        """
        return RetweetsOfTweetIdOperator(id)

    @classmethod
    def quotes_of_tweet_id(cls, id: TweetId) -> QuotesOfTweetIdOperator:
        """
        どのツイートへの引用ツイートかで絞り込む。
        """
        return QuotesOfTweetIdOperator(id)

    @overload
    @classmethod
    def context(
        cls,
        context: TweetContextAnnotation,
        *,
        domain_id: Literal[None] = None,
        entity_id: Literal[None] = None,
    ) -> ContextOperator:
        ...

    @overload
    @classmethod
    def context(
        cls,
        context: Literal[None] = None,
        *,
        domain_id: DomainId,
        entity_id: EntityId,
    ) -> ContextOperator:
        ...

    @classmethod
    def context(
        cls,
        context: Any = None,
        *,
        domain_id: Any = None,
        entity_id: Any = None,
    ) -> ContextOperator:
        return ContextOperator(
            context,
            domain_id=domain_id,
            entity_id=entity_id,
        )

    @classmethod
    def entity(cls, name: EntityName) -> EntityOperator:
        return EntityOperator(name)

    @classmethod
    def conversation_id(cls, id: DmConversationId) -> ConversationIdOperator:
        """
        どの DM 会話でのツイートかで絞り込む。
        """
        return ConversationIdOperator(id)

    @classmethod
    def list(cls, id: ListId) -> ListOperator:
        return ListOperator(id)

    @classmethod
    def place(cls, place: Union[PlaceId, PlaceName]) -> PlaceOperator:
        """
        どの場所でのツイートかで絞り込む。
        """
        return PlaceOperator(place)

    @classmethod
    def place_country(cls, code: PlaceCountryCode) -> PlaceCountryOperator:
        """
        どの国からのツイートかで絞り込む。
        """
        return PlaceCountryOperator(code)

    @overload
    @classmethod
    def point_radius(
        cls,
        *,
        longitude: float,
        latitude: float,
        radius_km: int,
        radius_mi: Literal[None] = None,
    ) -> PointRadiusOperator:
        ...

    @overload
    @classmethod
    def point_radius(
        cls,
        *,
        longitude: float,
        latitude: float,
        radius_km: Literal[None] = None,
        radius_mi: int,
    ) -> PointRadiusOperator:
        ...

    @classmethod
    def point_radius(
        cls,
        *,
        longitude: float,
        latitude: float,
        radius_km: Any = None,
        radius_mi: Any = None,
    ) -> PointRadiusOperator:
        """
        どの座標範囲からのツイートかで絞り込む。
        """
        return PointRadiusOperator(
            longitude=longitude,
            latitude=latitude,
            radius_km=radius_km,
            radius_mi=radius_mi,
        )

    @classmethod
    def bounding_box(
        cls,
        *,
        west_longitude: float,
        south_latitude: float,
        east_longitude: float,
        north_latitude: float,
    ) -> BoundingBoxOperator:
        """
        どの座標範囲からのツイートかで絞り込む。
        """
        return BoundingBoxOperator(
            west_longitude=west_longitude,
            south_latitude=south_latitude,
            east_longitude=east_longitude,
            north_latitude=north_latitude,
        )

    @classmethod
    def is_retweet(cls) -> IsRetweetOperator:
        """
        リツイートであるかどうかの絞り込み。

        単体では成立しないため、成立するクエリの右側に AND 結合する必要がある。
        """
        return IsRetweetOperator()

    @classmethod
    def is_reply(cls) -> IsReplyOperator:
        """
        返信ツイートであるかどうかの絞り込み。

        単体では成立しないため、成立するクエリの右側に AND 結合する必要がある。
        """
        return IsReplyOperator()

    @classmethod
    def is_quote(cls) -> IsQuoteOperator:
        """
        引用ツイートであるかどうかの絞り込み。

        単体では成立しないため、成立するクエリの右側に AND 結合する必要がある。
        """
        return IsQuoteOperator()

    @classmethod
    def is_verified(cls) -> IsVerifiedOperator:
        """
        認証ユーザのツイートであるかどうかの絞り込み。

        単体では成立しないため、成立するクエリの右側に AND 結合する必要がある。
        """
        return IsVerifiedOperator()

    @classmethod
    def is_nullcast(cls) -> IsNullcastOperator:
        """
        Nullcast であるかどうかの絞り込み。

        否定形としてしか使えないことに注意。
        単体では成立しないため、成立するクエリの右側に AND 結合する必要がある。
        """
        return IsNullcastOperator()

    @classmethod
    def has_hashtags(cls) -> HasHashtagsOperator:
        """
        ハッシュタグのついたツイートであるかどうかの絞り込み。

        単体では成立しないため、成立するクエリの右側に AND 結合する必要がある。
        """
        return HasHashtagsOperator()

    @classmethod
    def has_cashtags(cls) -> HasCashtagsOperator:
        """
        キャッシュタグのついたツイートであるかどうかの絞り込み。

        単体では成立しないため、成立するクエリの右側に AND 結合する必要がある。
        """
        return HasCashtagsOperator()

    @classmethod
    def has_links(cls) -> HasLinksOperator:
        """
        リンクのついたツイートであるかどうかの絞り込み。

        単体では成立しないため、成立するクエリの右側に AND 結合する必要がある。
        """
        return HasLinksOperator()

    @classmethod
    def has_mentions(cls) -> HasMentionsOperator:
        """
        メンションのついたツイートであるかどうかの絞り込み。

        単体では成立しないため、成立するクエリの右側に AND 結合する必要がある。
        """
        return HasMentionsOperator()

    @classmethod
    def has_media(cls) -> HasMediaOperator:
        """
        メディアのついたツイートであるかどうかの絞り込み。

        単体では成立しないため、成立するクエリの右側に AND 結合する必要がある。
        """
        return HasMediaOperator()

    @classmethod
    def has_images(cls) -> HasImagesOperator:
        """
        画像のついたツイートであるかどうかの絞り込み。

        単体では成立しないため、成立するクエリの右側に AND 結合する必要がある。
        """
        return HasImagesOperator()

    @classmethod
    def has_video_link(cls) -> HasVideoLinkOperator:
        """
        ビデオのついたツイートであるかどうかの絞り込み。

        単体では成立しないため、成立するクエリの右側に AND 結合する必要がある。
        """
        return HasVideoLinkOperator()

    @classmethod
    def has_geo(cls) -> HasGeoOperator:
        """
        位置情報のついたツイートであるかどうかの絞り込み。

        単体では成立しないため、成立するクエリの右側に AND 結合する必要がある。
        """
        return HasGeoOperator()

    @classmethod
    def lang(cls, lang: Language) -> LangOperator:
        """
        言語による絞り込み。

        単体では成立しないため、成立するクエリの右側に AND 結合する必要がある。
        """
        return LangOperator(lang)
