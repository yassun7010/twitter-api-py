from abc import abstractmethod
from typing import Any, Callable, Literal, Type, Union, overload

from twitter_api.types.v2_dm_conversation.dm_conversation_id import DmConversationId
from twitter_api.types.v2_domain import DomainId
from twitter_api.types.v2_entity.entity_id import EntityId
from twitter_api.types.v2_entity.entity_name import EntityName
from twitter_api.types.v2_list.list_id import ListId
from twitter_api.types.v2_place.place_country_code import PlaceCountryCode
from twitter_api.types.v2_place.place_id import PlaceId
from twitter_api.types.v2_place.place_name import PlaceName
from twitter_api.types.v2_search_query.operators.place_country_operator import (
    PlaceCountryOperator,
)
from twitter_api.types.v2_search_query.operators.place_operator import PlaceOperator
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
from .operators.operator import Operator
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
            Union[Operator, tuple[Operator, ...]],
        ],
    ):
        """
        クエリを組み立てる。

        >>> from .search_query import SearchQuery
        >>> query = SearchQuery.build(
        ...     lambda q: (
        ...         q.group(
        ...             q.hashtag("#Twitter") | q.hashtag("Xcorp"),
        ...         )
        ...         & q.mention("@elonmusk")
        ...         & ~q.mention("SpaceX")
        ...     )
        ... )
        >>> str(query)
        '(#Twitter OR #Xcorp) @elonmusk -@SpaceX'
        """

        query = building(_SearchQueryBuilder)
        if isinstance(query, tuple):
            return SearchQuery(*query)
        else:
            return SearchQuery(query)


class _SearchQueryBuilder:
    @abstractmethod
    def __init__(self) -> None:
        pass

    @classmethod
    def keyword(cls, keyword: str) -> KeywordOperator:
        return KeywordOperator(keyword)

    @classmethod
    def mention(cls, username: Username) -> MentionOperator:
        return MentionOperator(username)

    @classmethod
    def hashtag(cls, hashtag: str) -> HashtagOperator:
        return HashtagOperator(hashtag)

    @classmethod
    def cashtag(cls, cashtag: str) -> CashtagOperator:
        return CashtagOperator(cashtag)

    @classmethod
    def group(cls, *operators: Operator) -> GroupOperator:
        return GroupOperator(*operators)

    @classmethod
    def from_user(cls, user: Union[UserId, Username]) -> FromUserOperator:
        return FromUserOperator(user)

    @classmethod
    def to_user(cls, user: Union[UserId, Username]) -> ToUserOperator:
        return ToUserOperator(user)

    @classmethod
    def url(cls, url: str) -> UrlOperator:
        return UrlOperator(url)

    @classmethod
    def retweet_of(cls, user: Union[UserId, Username]) -> RetweetOfOperator:
        return RetweetOfOperator(user)

    @classmethod
    def in_reply_to_tweet_id(cls, id: TweetId) -> InReplyToTweetIdOperator:
        return InReplyToTweetIdOperator(id)

    @classmethod
    def retweets_of_tweet_id(cls, id: TweetId) -> RetweetsOfTweetIdOperator:
        return RetweetsOfTweetIdOperator(id)

    @classmethod
    def quotes_of_tweet_id(cls, id: TweetId) -> QuotesOfTweetIdOperator:
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
        return ConversationIdOperator(id)

    @classmethod
    def list(cls, id: ListId) -> ListOperator:
        return ListOperator(id)

    @classmethod
    def place(cls, place: Union[PlaceId, PlaceName]) -> PlaceOperator:
        return PlaceOperator(place)

    @classmethod
    def place_country(cls, code: PlaceCountryCode) -> PlaceCountryOperator:
        return PlaceCountryOperator(code)
