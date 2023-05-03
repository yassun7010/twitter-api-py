from twitter_api.types.v2_search_query.mention import Mention
from twitter_api.types.v2_search_query.search_query import SearchQuery


class TestMention:
    def test_mention(self):
        assert str(Mention("elonmusk")) == "@elonmusk"

    def test_mention_with_mark(self):
        assert str(Mention("@elonmusk")) == "@elonmusk"

    def test_query_build(self):
        assert str(SearchQuery.build(lambda q: q.mention("elonmusk"))) == "@elonmusk"
