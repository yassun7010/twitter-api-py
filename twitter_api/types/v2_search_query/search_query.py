from abc import abstractmethod
from typing import Callable, Type, Union

from twitter_api.types.v2_search_query.cashtag import Cashtag
from twitter_api.types.v2_search_query.from_user import FromUser
from twitter_api.types.v2_search_query.group import Group, grouping
from twitter_api.types.v2_search_query.hashtag import Hashtag
from twitter_api.types.v2_search_query.in_reply_to_tweet_id import InReplyToTweetId
from twitter_api.types.v2_search_query.keyword import Keyword
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
