from twitter_api.types.v2_search_query.operators.mention_operator import MentionOperator
from twitter_api.types.v2_search_query.operators.operator import CompleteOperator
from twitter_api.types.v2_search_query.search_query import SearchQuery, build


class TestMentionOperator:
    def test_mention_operator(self):
        assert str(MentionOperator("twitterdev")) == "@twitterdev"

    def test_mention_operator_with_mark(self):
        assert str(MentionOperator("@twitterdev")) == "@twitterdev"

    def test_query_complete(self):
        assert isinstance(
            build(lambda q: q.mention("twitterdev")),
            CompleteOperator,
        )

    def test_query_build(self):
        assert (
            str(SearchQuery.build(lambda q: q.mention("twitterdev"))) == "@twitterdev"
        )
