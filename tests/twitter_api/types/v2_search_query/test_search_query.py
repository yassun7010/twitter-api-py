import pytest

from twitter_api.types.v2_search_query.operators.keyword_operator import KeywordOperator
from twitter_api.types.v2_search_query.operators.mention_operator import MentionOperator
from twitter_api.types.v2_search_query.operators.operator import (
    CorrectOperator,
    WeakOperator,
)
from twitter_api.types.v2_search_query.search_query import (
    SearchQuery,
    _SearchQueryBuilder,
)


class TestSearchQuery:
    def test_search_query_operator(self):
        query = SearchQuery(
            KeywordOperator("twitter")
            & MentionOperator("elonmusk")
            & ~MentionOperator("SpaceX"),
        )

        assert str(query) == "twitter @elonmusk -@SpaceX"

    def test_search_query_comma_separator(self):
        query = SearchQuery(
            KeywordOperator("twitter"),
            MentionOperator("elonmusk"),
            ~MentionOperator("SpaceX"),
        )

        assert str(query) == "twitter @elonmusk -@SpaceX"


class TestSearchQueryBuilder:
    def test_constructor(self):
        with pytest.raises(TypeError):
            _SearchQueryBuilder()  # type: ignore

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
            == "SearchQuery(AndOperator(CorrectGroupOperator(CorrectOrOperator(KeywordOperator('\"Twitter API\"'), HashtagOperator('#v2'))), NotOperator(IsRetweetOperator('is:retweet'))))"
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

    def test_query_builder_correct_or_correct(self):
        assert isinstance(
            _SearchQueryBuilder.mention("twitterdev")
            | _SearchQueryBuilder.hashtag("Twitter"),
            CorrectOperator,
        )

    def test_query_builder_correct_or_weak(self):
        assert isinstance(
            _SearchQueryBuilder.mention("twitterdev") | _SearchQueryBuilder.is_quote(),
            WeakOperator,
        )

    def test_query_builder_weak_or_correct(self):
        assert isinstance(
            _SearchQueryBuilder.is_retweet()
            | _SearchQueryBuilder.mention("twitterdev"),
            WeakOperator,
        )

    def test_query_builder_weak_or_weak(self):
        assert isinstance(
            _SearchQueryBuilder.is_retweet() | _SearchQueryBuilder.is_quote(),
            WeakOperator,
        )
