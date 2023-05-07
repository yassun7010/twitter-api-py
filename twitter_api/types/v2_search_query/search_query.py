from typing import Any, Callable, Literal, Union, overload

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
from .operators.group_operator import (
    CorrectGroupOperator,
    GroupOperator,
    WeakGroupOperator,
)
from .operators.hashtag_operator import HashtagOperator
from .operators.in_reply_to_tweet_id_operator import InReplyToTweetIdOperator
from .operators.keyword_operator import KeywordOperator
from .operators.list_operator import ListOperator
from .operators.mention_operator import MentionOperator
from .operators.operator import CorrectOperator, Operator, WeakOperator
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

    def __init__(self, query: Operator) -> None:
        self._query = query

    def __str__(self) -> str:
        # ルートが Group の場合は括弧で囲まない。
        if isinstance(self._query, GroupOperator):
            return str(self._query._operator)
        else:
            return str(self._query)

    def __repr__(self):
        return f"{self.__class__.__name__}({repr(self._query)})"

    @classmethod
    def build(
        cls,
        building: Callable[["SearchQueryBuilder"], CorrectOperator],
    ):
        """
        検索クエリを組み立てる。

        静的解析でエラーを出さずにクエリを組み立てるには、下記のルールに従う。

        - AND 演算（ & 結合）は左右のどちらかがクエリとして成立する場合、結合結果もクエリとして成立する。
        - OR 演算（ | 結合）は左右の両方がクエリとして成立する場合、結合結果もクエリとして成立する。
        - NOT 演算（ ~ ）により否定された要素は、単体ではクエリとして成立しない。
        - グループで囲まれた要素は先に評価される。
        - 二重否定、グループへの否定はできない。

        >>> from .search_query import SearchQuery
        >>> query = SearchQuery.build(
        ...     lambda q: (
        ...         q.keyword("day")
        ...         & q.group(
        ...             q.hashtag("#Twitter") | q.hashtag("Xcorp"),
        ...         )
        ...         & q.mention("@elonmusk")
        ...         & ~q.mention("SpaceX")
        ...         & q.is_retweet()
        ...     )
        ... )
        >>> str(query)
        'day (#Twitter OR #Xcorp) @elonmusk -@SpaceX is:retweet'
        """

        return SearchQuery(build(building))


class SearchQueryBuilder:
    def keyword(self, keyword: str) -> KeywordOperator:
        """
        キーワードによる絞り込み。

        空白が含まれる場合、ダブルクォーテーションで囲まれる。
        """
        return KeywordOperator(keyword)

    def mention(self, username: Username) -> MentionOperator:
        """
        メンションによる絞り込み。

        先頭に @ がない場合、 @ をつけて処理される。
        """
        return MentionOperator(username)

    def hashtag(self, hashtag: Hashtag) -> HashtagOperator:
        """
        ハッシュタグによる絞り込み。

        先頭に # がない場合、 # をつけて処理される。
        """
        return HashtagOperator(hashtag)

    def cashtag(self, cashtag: Cashtag) -> CashtagOperator:
        """
        キャッシュタグによる絞り込み。

        先頭に $ がない場合、 $ をつけて処理される。
        """
        return CashtagOperator(cashtag)

    @overload
    def group(self, operator: CorrectOperator) -> CorrectGroupOperator:
        ...

    @overload
    def group(self, operator: WeakOperator) -> WeakGroupOperator:
        ...

    def group(self, operator: Union[CorrectOperator, WeakOperator]):
        """
        括弧で囲みたい対象を指定する。括弧で囲まれた対象は優先的に計算される。

        要素数が 1 つの場合は括弧をつけない。
        """
        if isinstance(operator, CorrectOperator):
            return CorrectGroupOperator(operator)
        else:
            return WeakGroupOperator(operator)

    def from_user(self, user: Union[UserId, Username]) -> FromUserOperator:
        """
        どのユーザからツイートされたかで絞り込む。
        """
        return FromUserOperator(user)

    def to_user(self, user: Union[UserId, Username]) -> ToUserOperator:
        """
        どのユーザへツイートしたかで絞り込む。
        """
        return ToUserOperator(user)

    def url(self, url: str) -> UrlOperator:
        """
        ツイートに含まれる URL で絞り込む。
        """
        return UrlOperator(url)

    def retweet_of(self, user: Union[UserId, Username]) -> RetweetOfOperator:
        """
        どのユーザへのリツイートかで絞り込む。
        """
        return RetweetOfOperator(user)

    def in_reply_to_tweet_id(self, id: TweetId) -> InReplyToTweetIdOperator:
        """
        どのツイートへのリプライかで絞り込む。
        """
        return InReplyToTweetIdOperator(id)

    def retweets_of_tweet_id(self, id: TweetId) -> RetweetsOfTweetIdOperator:
        """
        どのツイートへのリツイートかで絞り込む。
        """
        return RetweetsOfTweetIdOperator(id)

    def quotes_of_tweet_id(self, id: TweetId) -> QuotesOfTweetIdOperator:
        """
        どのツイートへの引用ツイートかで絞り込む。
        """
        return QuotesOfTweetIdOperator(id)

    @overload
    def context(
        self,
        context: TweetContextAnnotation,
        *,
        domain_id: Literal[None] = None,
        entity_id: Literal[None] = None,
    ) -> ContextOperator:
        ...

    @overload
    def context(
        self,
        context: Literal[None] = None,
        *,
        domain_id: DomainId,
        entity_id: EntityId,
    ) -> ContextOperator:
        ...

    def context(
        self,
        context: Any = None,
        *,
        domain_id: Any = None,
        entity_id: Any = None,
    ) -> ContextOperator:
        """
        ツイートの持つコンテキスト情報による絞り込み。

        refer: https://developer.twitter.com/en/docs/twitter-api/annotations/overview
        """
        return ContextOperator(
            context,
            domain_id=domain_id,
            entity_id=entity_id,
        )

    def entity(self, name: EntityName) -> EntityOperator:
        """
        エンティティによる絞り込み。

        refer: https://developer.twitter.com/en/docs/twitter-api/annotations/overview
        """
        return EntityOperator(name)

    def conversation_id(self, id: DmConversationId) -> ConversationIdOperator:
        """
        どの DM 会話でのツイートかで絞り込む。
        """
        return ConversationIdOperator(id)

    def list(self, id: ListId) -> ListOperator:
        """
        指定したリストに入っているユーザのツイートかで絞り込む。

        リストに関しては、下記のリンクを参照。

        refer: https://developer.twitter.com/en/docs/twitter-api/lists/list-lookup/api-reference
        refer: https://developer.twitter.com/en/docs/twitter-api/lists/manage-lists/api-reference
        """
        return ListOperator(id)

    def place(self, place: Union[PlaceId, PlaceName]) -> PlaceOperator:
        """
        どの場所でのツイートかで絞り込む。
        """
        return PlaceOperator(place)

    def place_country(self, code: PlaceCountryCode) -> PlaceCountryOperator:
        """
        どの国からのツイートかで絞り込む。
        """
        return PlaceCountryOperator(code)

    @overload
    def point_radius(
        self,
        *,
        longitude_deg: float,
        latitude_deg: float,
        radius_km: int,
        radius_mi: Literal[None] = None,
    ) -> PointRadiusOperator:
        ...

    @overload
    def point_radius(
        self,
        *,
        longitude_deg: float,
        latitude_deg: float,
        radius_km: Literal[None] = None,
        radius_mi: int,
    ) -> PointRadiusOperator:
        ...

    def point_radius(
        self,
        *,
        longitude_deg: float,
        latitude_deg: float,
        radius_km: Any = None,
        radius_mi: Any = None,
    ) -> PointRadiusOperator:
        """
        どの位置座標からのツイートかで絞り込む。

        - `longitude` の範囲： ±180[deg]
        - `latitude` の範囲： ±90[deg]
        """
        return PointRadiusOperator(
            longitude_deg=longitude_deg,
            latitude_deg=latitude_deg,
            radius_km=radius_km,
            radius_mi=radius_mi,
        )

    def bounding_box(
        self,
        *,
        west_longitude_deg: float,
        south_latitude_deg: float,
        east_longitude_deg: float,
        north_latitude_deg: float,
    ) -> BoundingBoxOperator:
        """
        どの地図範囲からのツイートかで絞り込む。

        - `longitude` の範囲： ±180[deg]
        - `latitude` の範囲： ±90[deg]
        """
        return BoundingBoxOperator(
            west_longitude_deg=west_longitude_deg,
            south_latitude_deg=south_latitude_deg,
            east_longitude_deg=east_longitude_deg,
            north_latitude_deg=north_latitude_deg,
        )

    def is_retweet(self) -> IsRetweetOperator:
        """
        リツイートであるかどうかの絞り込み。

        単体では成立しないため、成立する他のクエリと AND 結合する必要がある。
        """
        return IsRetweetOperator()

    def is_reply(self) -> IsReplyOperator:
        """
        返信ツイートであるかどうかの絞り込み。

        単体では成立しないため、成立する他のクエリと AND 結合する必要がある。
        """
        return IsReplyOperator()

    def is_quote(self) -> IsQuoteOperator:
        """
        引用ツイートであるかどうかの絞り込み。

        単体では成立しないため、成立する他のクエリと AND 結合する必要がある。
        """
        return IsQuoteOperator()

    def is_verified(self) -> IsVerifiedOperator:
        """
        認証ユーザのツイートであるかどうかの絞り込み。

        単体では成立しないため、成立する他のクエリと AND 結合する必要がある。
        """
        return IsVerifiedOperator()

    def is_nullcast(self) -> IsNullcastOperator:
        """
        Nullcast であるかどうかの絞り込み。

        否定形としてしか使えないことに注意。
        単体では成立しないため、成立する他のクエリと AND 結合する必要がある。
        """
        return IsNullcastOperator()

    def has_hashtags(self) -> HasHashtagsOperator:
        """
        ハッシュタグのついたツイートであるかどうかの絞り込み。

        単体では成立しないため、成立する他のクエリと AND 結合する必要がある。
        """
        return HasHashtagsOperator()

    def has_cashtags(self) -> HasCashtagsOperator:
        """
        キャッシュタグのついたツイートであるかどうかの絞り込み。

        単体では成立しないため、成立する他のクエリと AND 結合する必要がある。
        """
        return HasCashtagsOperator()

    def has_links(self) -> HasLinksOperator:
        """
        リンクのついたツイートであるかどうかの絞り込み。

        単体では成立しないため、成立する他のクエリと AND 結合する必要がある。
        """
        return HasLinksOperator()

    def has_mentions(self) -> HasMentionsOperator:
        """
        メンションのついたツイートであるかどうかの絞り込み。

        単体では成立しないため、成立する他のクエリと AND 結合する必要がある。
        """
        return HasMentionsOperator()

    def has_media(self) -> HasMediaOperator:
        """
        メディアのついたツイートであるかどうかの絞り込み。

        単体では成立しないため、成立する他のクエリと AND 結合する必要がある。
        """
        return HasMediaOperator()

    def has_images(self) -> HasImagesOperator:
        """
        画像のついたツイートであるかどうかの絞り込み。

        単体では成立しないため、成立する他のクエリと AND 結合する必要がある。
        """
        return HasImagesOperator()

    def has_video_link(self) -> HasVideoLinkOperator:
        """
        ビデオのついたツイートであるかどうかの絞り込み。

        単体では成立しないため、成立する他のクエリと AND 結合する必要がある。
        """
        return HasVideoLinkOperator()

    def has_geo(self) -> HasGeoOperator:
        """
        位置情報のついたツイートであるかどうかの絞り込み。

        単体では成立しないため、成立する他のクエリと AND 結合する必要がある。
        """
        return HasGeoOperator()

    def lang(self, lang: Language) -> LangOperator:
        """
        言語による絞り込み。

        単体では成立しないため、成立する他のクエリと AND 結合する必要がある。
        """
        return LangOperator(lang)


def build(building: Callable[[SearchQueryBuilder], Operator]) -> Operator:
    return building(SearchQueryBuilder())
