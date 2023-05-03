from twitter_api.types.v2_search_query.keyword import Keyword
from twitter_api.types.v2_search_query.mention import Mention
from twitter_api.types.v2_search_query.search_query import SearchQuery


class TestSearchQuery:
    def test_search_query_operator(self):
        query = SearchQuery(
            Keyword("twitter") & Mention("elonmusk") & ~Mention("SpaceX"),
        )

        assert str(query) == "twitter @elonmusk -@SpaceX"

    def test_search_query_comma_separator(self):
        query = SearchQuery(
            Keyword("twitter"),
            Mention("elonmusk"),
            ~Mention("SpaceX"),
        )

        assert str(query) == "twitter @elonmusk -@SpaceX"

    def test_search_query_building(self):
        query = SearchQuery.build(
            lambda q: (
                q.keyword("twitter") & q.mention("elonmusk") & ~q.mention("SpaceX"),
            )
        )

        assert str(query) == "twitter @elonmusk -@SpaceX"
