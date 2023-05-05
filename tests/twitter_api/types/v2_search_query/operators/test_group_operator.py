from twitter_api.types.v2_search_query.operators.group_operator import (
    CorrectGroupOperator,
)
from twitter_api.types.v2_search_query.operators.keyword_operator import KeywordOperator
from twitter_api.types.v2_search_query.operators.mention_operator import MentionOperator
from twitter_api.types.v2_search_query.search_query import SearchQuery


class TestGroupOperator:
    def test_group_operator_single_len(self):
        assert (
            len(
                CorrectGroupOperator(
                    KeywordOperator("twitter") & MentionOperator("elonmusk")
                )
            )
            == 1
        )

    def test_group_operator_multiple_len(self):
        assert (
            len(
                CorrectGroupOperator(
                    KeywordOperator("twitter"), MentionOperator("elonmusk")
                )
            )
            == 2
        )

    def test_group_operator_single_operator(self):
        query = SearchQuery(CorrectGroupOperator(MentionOperator("SpaceX")))

        assert str(query) == "@SpaceX"

    def test_group_operator_and_operator(self):
        query = SearchQuery(
            CorrectGroupOperator(
                KeywordOperator("twitter") & MentionOperator("elonmusk")
            )
            & ~MentionOperator("SpaceX"),
        )

        assert str(query) == "(twitter @elonmusk) -@SpaceX"

    def test_group_operator_and_comma_separated(self):
        query = SearchQuery(
            CorrectGroupOperator(
                KeywordOperator("twitter") & MentionOperator("elonmusk")
            ),
            ~MentionOperator("SpaceX"),
        )

        assert str(query) == "(twitter @elonmusk) -@SpaceX"

    def test_group_operator_or_comma_separated(self):
        query = SearchQuery(
            CorrectGroupOperator(
                KeywordOperator("twitter") | MentionOperator("elonmusk")
            ),
            ~MentionOperator("SpaceX"),
        )

        assert str(query) == "(twitter OR @elonmusk) -@SpaceX"

    def test_group_operator_nest_comma_separated(self):
        query = SearchQuery(
            CorrectGroupOperator(
                KeywordOperator("twitter"), MentionOperator("elonmusk")
            ),
            ~MentionOperator("SpaceX"),
        )

        assert str(query) == "(twitter @elonmusk) -@SpaceX"

    def test_group_operator_comma_separated(self):
        query = SearchQuery(
            CorrectGroupOperator(
                KeywordOperator("twitter"), MentionOperator("elonmusk")
            )
        )

        assert str(query) == "(twitter @elonmusk)"

    def test_search_query_builder_correct_group(self):
        query = SearchQuery.build(
            lambda q: q.group(q.keyword("twitter") & q.mention("twitterdev"))
        )

        assert str(query) == "(twitter @twitterdev)"

    def test_search_query_builder_weak_group(self):
        query = SearchQuery.build(
            lambda q: (
                q.mention("twitterdev")
                & q.group(
                    q.is_quote() | q.is_reply() | q.is_retweet(),
                )
            )
        )

        assert str(query) == "@twitterdev (is:quote OR is:reply OR is:retweet)"
