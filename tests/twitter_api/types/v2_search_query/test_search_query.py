from twitter_api.types.v2_search_query.operators.keyword_operator import KeywordOperator
from twitter_api.types.v2_search_query.operators.mention_operator import MentionOperator
from twitter_api.types.v2_search_query.operators.operator import (
    CompleteOperator,
    IncompleteOperator,
)
from twitter_api.types.v2_search_query.search_query import SearchQuery, build


class TestSearchQuery:
    def test_search_query_operator(self):
        query = SearchQuery(
            KeywordOperator("twitter")
            & MentionOperator("elonmusk")
            & ~MentionOperator("SpaceX"),
        )

        assert str(query) == "twitter @elonmusk -@SpaceX"


class TestSearchQueryBuilder:
    def test_search_query_builder(self):
        query = SearchQuery.build(
            lambda q: (
                q.keyword("twitter") & q.mention("elonmusk") & ~q.mention("SpaceX")
            )
        )

        assert str(query) == "twitter @elonmusk -@SpaceX"

    def test_search_query_builder_with_group(self):
        query = SearchQuery.build(
            lambda q: (
                q.group(
                    q.hashtag("#Twitter") | q.hashtag("Xcorp"),
                )
                & q.mention("@elonmusk")
                & ~q.mention("SpaceX")
            )
        )

        assert str(query) == "(#Twitter OR #Xcorp) @elonmusk -@SpaceX"

    def test_search_query_builder_complex(self):
        query = SearchQuery.build(
            lambda q: (
                q.group(
                    q.group(
                        q.hashtag("#Twitter") | q.hashtag("Xcorp"),
                    )
                    & q.mention("@elonmusk")
                    & ~q.mention("SpaceX")
                )
                & q.is_retweet()
                & ~q.is_nullcast()
            )
        )

        assert (
            str(query)
            == "((#Twitter OR #Xcorp) @elonmusk -@SpaceX) is:retweet -is:nullcast"
        )

    def test_query_builder_repr(self):
        assert (
            repr(
                SearchQuery.build(
                    lambda q: (
                        q.group(
                            q.keyword("Twitter API") | q.hashtag("v2"),
                        )
                        & ~q.is_retweet()
                    )
                )
            )
            == "SearchQuery(CompleteAndOperator(CompleteGroupOperator(CompleteOrOperator(KeywordOperator('\"Twitter API\"'), HashtagOperator('#v2'))), NotOperator(IsRetweetOperator('is:retweet'))))"
        )

    def test_query_builder_emoji_keyword(self):
        assert (
            str(
                SearchQuery.build(
                    lambda q: (
                        q.group(
                            q.keyword("😃") | q.keyword("😡"),
                        )
                        & q.keyword("😬")
                    )
                )
            )
            == "(😃 OR 😡) 😬"
        )

    def test_query_builder_exact_phrase_match_keyword(self):
        assert (
            str(
                SearchQuery.build(
                    lambda q: (
                        q.group(
                            q.keyword("Twitter API") | q.hashtag("v2"),
                        )
                        & ~q.keyword("recent search")
                    )
                )
            )
            == '("Twitter API" OR #v2) -"recent search"'
        )

    def test_query_builder_complete_and_complete(self):
        assert isinstance(
            build(lambda q: (q.mention("twitterdev") & q.hashtag("Twitter"))),
            CompleteOperator,
        )

    def test_query_builder_complete_and_incomplete(self):
        assert isinstance(
            build(lambda q: (q.mention("twitterdev") & q.is_quote())),
            CompleteOperator,
        )

    def test_query_builder_incomplete_and_complete(self):
        assert isinstance(
            build(lambda q: (q.is_retweet() & q.mention("twitterdev"))),
            CompleteOperator,
        )

    def test_query_builder_incomplete_and_incomplete(self):
        assert isinstance(
            build(lambda q: (q.is_retweet() & q.is_quote())),
            IncompleteOperator,
        )

    def test_query_builder_complete_or_complete(self):
        assert isinstance(
            build(lambda q: (q.mention("twitterdev") | q.hashtag("Twitter"))),
            CompleteOperator,
        )

    def test_query_builder_complete_or_incomplete(self):
        assert isinstance(
            build(lambda q: (q.mention("twitterdev") | q.is_quote())),
            IncompleteOperator,
        )

    def test_query_builder_incomplete_or_complete(self):
        assert isinstance(
            build(lambda q: (q.is_retweet() | q.mention("twitterdev"))),
            IncompleteOperator,
        )

    def test_query_builder_incomplete_or_incomplete(self):
        assert isinstance(
            build(lambda q: (q.is_retweet() | q.is_quote())),
            IncompleteOperator,
        )

    def test_query_builder_and_or_priority(self):
        query = build(lambda q: (q.mention("twitterdev") & q.is_reply() | q.is_quote()))

        assert isinstance(query, IncompleteOperator)
        assert str(query) == "@twitterdev is:reply OR is:quote"

    def test_query_builder_and_or_priority2(self):
        query = build(
            lambda q: (q.mention("twitterdev") & q.group(q.is_reply() | q.is_quote()))
        )

        assert isinstance(query, CompleteOperator)
        assert str(query) == "@twitterdev (is:reply OR is:quote)"
