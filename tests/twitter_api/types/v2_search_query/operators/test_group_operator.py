from twitter_api.types.v2_search_query.operators.group_operator import GroupOperator
from twitter_api.types.v2_search_query.operators.keyword_operator import KeywordOperator
from twitter_api.types.v2_search_query.operators.mention_operator import MentionOperator
from twitter_api.types.v2_search_query.search_query import SearchQuery


class TestGroup:
    def test_group_single_len(self):
        assert (
            len(GroupOperator(KeywordOperator("twitter") & MentionOperator("elonmusk")))
            == 1
        )

    def test_group_multiple_len(self):
        assert (
            len(GroupOperator(KeywordOperator("twitter"), MentionOperator("elonmusk")))
            == 2
        )

    def test_group_not_operator(self):
        query = SearchQuery(GroupOperator(~MentionOperator("SpaceX")))

        assert str(query) == "(-@SpaceX)"

    def test_group_and_operator(self):
        query = SearchQuery(
            GroupOperator(KeywordOperator("twitter") & MentionOperator("elonmusk"))
            & ~MentionOperator("SpaceX"),
        )

        assert str(query) == "(twitter @elonmusk) -@SpaceX"

    def test_group_and_comma_separated(self):
        query = SearchQuery(
            GroupOperator(KeywordOperator("twitter") & MentionOperator("elonmusk")),
            ~MentionOperator("SpaceX"),
        )

        assert str(query) == "(twitter @elonmusk) -@SpaceX"

    def test_group_or_comma_separated(self):
        query = SearchQuery(
            GroupOperator(KeywordOperator("twitter") | MentionOperator("elonmusk")),
            ~MentionOperator("SpaceX"),
        )

        assert str(query) == "(twitter OR @elonmusk) -@SpaceX"

    def test_group_nest_comma_separated(self):
        query = SearchQuery(
            GroupOperator(KeywordOperator("twitter"), MentionOperator("elonmusk")),
            ~MentionOperator("SpaceX"),
        )

        assert str(query) == "(twitter @elonmusk) -@SpaceX"

    def test_group_comma_separated(self):
        query = SearchQuery(
            GroupOperator(KeywordOperator("twitter"), MentionOperator("elonmusk"))
        )

        assert str(query) == "(twitter @elonmusk)"
