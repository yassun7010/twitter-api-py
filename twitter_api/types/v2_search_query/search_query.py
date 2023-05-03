from abc import abstractmethod
from typing import Any, Callable, Literal, Optional, Type, Union, overload

from twitter_api.types.v2_dm_conversation.dm_conversation_id import DmConversationId
from twitter_api.types.v2_domain import DomainId
from twitter_api.types.v2_entity.entity_id import EntityId
from twitter_api.types.v2_entity.entity_name import EntityName
from twitter_api.types.v2_list.list_id import ListId
from twitter_api.types.v2_search_query.cashtag import Cashtag
from twitter_api.types.v2_search_query.context import Context
from twitter_api.types.v2_search_query.conversation_id import ConversationId
from twitter_api.types.v2_search_query.entity import Entity
from twitter_api.types.v2_search_query.from_user import FromUser
from twitter_api.types.v2_search_query.group import Group, grouping
from twitter_api.types.v2_search_query.hashtag import Hashtag
from twitter_api.types.v2_search_query.in_reply_to_tweet_id import InReplyToTweetId
from twitter_api.types.v2_search_query.keyword import Keyword
from twitter_api.types.v2_search_query.list import List
from twitter_api.types.v2_search_query.mention import Mention
from twitter_api.types.v2_search_query.operator import Operator
from twitter_api.types.v2_search_query.quotes_of_tweet_id import QuotesOfTweetId
from twitter_api.types.v2_search_query.retweet_of import RetweetOf
from twitter_api.types.v2_search_query.retweets_of_tweet_id import RetweetsOfTweetId
from twitter_api.types.v2_search_query.to_user import ToUser
from twitter_api.types.v2_search_query.url import Url
from twitter_api.types.v2_tweet.tweet_id import TweetId
from twitter_api.types.v2_user.user_id import UserId
from twitter_api.types.v2_user.username import Username


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

        >>> from twitter_api.types.v2_search_query.search_query import SearchQuery
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
    def keyword(cls, keyword: str) -> Keyword:
        return Keyword(keyword)

    @classmethod
    def mention(cls, username: Username) -> Mention:
        return Mention(username)

    @classmethod
    def hashtag(cls, hashtag: str) -> Hashtag:
        return Hashtag(hashtag)

    @classmethod
    def cashtag(cls, cashtag: str) -> Cashtag:
        return Cashtag(cashtag)

    @classmethod
    def group(cls, *operators: Operator) -> Group:
        return Group(*operators)

    @classmethod
    def from_user(cls, user: Union[UserId, Username]) -> FromUser:
        return FromUser(user)

    @classmethod
    def to_user(cls, user: Union[UserId, Username]) -> ToUser:
        return ToUser(user)

    @classmethod
    def url(cls, url: str) -> Url:
        return Url(url)

    @classmethod
    def retweet_of(cls, user: Union[UserId, Username]) -> RetweetOf:
        return RetweetOf(user)

    @classmethod
    def in_reply_to_tweet_id(cls, id: TweetId) -> InReplyToTweetId:
        return InReplyToTweetId(id)

    @classmethod
    def retweets_of_tweet_id(cls, id: TweetId) -> RetweetsOfTweetId:
        return RetweetsOfTweetId(id)

    @classmethod
    def quotes_of_tweet_id(cls, id: TweetId) -> QuotesOfTweetId:
        return QuotesOfTweetId(id)

    @overload
    @classmethod
    def context(
        cls,
        context: str,
        *,
        domain_id: Literal[None] = None,
        entity_id: Literal[None] = None,
    ) -> Context:
        ...

    @overload
    @classmethod
    def context(
        cls, context: Optional[str] = None, *, domain_id: DomainId, entity_id: EntityId
    ) -> Context:
        ...

    @classmethod
    def context(
        cls,
        context: Any = None,
        *,
        domain_id: Any = None,
        entity_id: Any = None,
    ) -> Context:
        return Context(
            context,
            domain_id=domain_id,
            entity_id=entity_id,
        )

    @classmethod
    def entity(cls, name: EntityName) -> Entity:
        return Entity(name)

    @classmethod
    def conversation_id(cls, id: DmConversationId) -> ConversationId:
        return ConversationId(id)

    @classmethod
    def list(cls, id: ListId) -> List:
        return List(id)
