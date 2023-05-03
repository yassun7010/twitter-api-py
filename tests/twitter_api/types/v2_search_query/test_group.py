from twitter_api.types.v2_search_query.group import Group
from twitter_api.types.v2_search_query.keyword import Keyword
from twitter_api.types.v2_search_query.mention import Mention
from twitter_api.types.v2_search_query.search_query import SearchQuery


class TestGroup:
    def test_group_single_len(self):
        assert len(Group(Keyword("twitter") & Mention("elonmusk"))) == 1

    def test_group_multiple_len(self):
        assert len(Group(Keyword("twitter"), Mention("elonmusk"))) == 2

    def test_group_and_operated(self):
        query = SearchQuery(
            Group(Keyword("twitter") & Mention("elonmusk")) & ~Mention("SpaceX"),
        )

        assert str(query) == "(twitter @elonmusk) -@SpaceX"

    def test_group_and_comma_separated(self):
        query = SearchQuery(
            Group(Keyword("twitter") & Mention("elonmusk")),
            ~Mention("SpaceX"),
        )

        assert str(query) == "(twitter @elonmusk) -@SpaceX"

    def test_group_or_comma_separated(self):
        query = SearchQuery(
            Group(Keyword("twitter") | Mention("elonmusk")),
            ~Mention("SpaceX"),
        )

        assert str(query) == "(twitter OR @elonmusk) -@SpaceX"

    def test_group_nest_comma_separated(self):
        query = SearchQuery(
            Group(Keyword("twitter"), Mention("elonmusk")),
            ~Mention("SpaceX"),
        )

        assert str(query) == "(twitter @elonmusk) -@SpaceX"

    def test_group_comma_separated(self):
        query = SearchQuery(Group(Keyword("twitter"), Mention("elonmusk")))

        assert str(query) == "(twitter @elonmusk)"
