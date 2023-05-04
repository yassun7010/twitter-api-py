from twitter_api.types.v2_search_query.operators.has_mentions_operator import (
    HasMentionsOperator,
)
from twitter_api.types.v2_search_query.search_query import SearchQuery


class TestHasMentionsOperator:
    def test_has_mentions_operator(self):
        assert str(HasMentionsOperator()) == "has:mentions"

    def test_query_build(self):
        assert (
            str(SearchQuery.build(lambda q: q.mention("twitterdev") & q.has_mentions()))
            == "@twitterdev has:mentions"
        )
