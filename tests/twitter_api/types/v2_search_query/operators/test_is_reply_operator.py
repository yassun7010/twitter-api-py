from twitter_api.types.v2_search_query.operators.is_reply_operator import (
    IsReplyOperator,
)
from twitter_api.types.v2_search_query.operators.operator import IncompleteOperator
from twitter_api.types.v2_search_query.search_query import SearchQuery, build


class TestIsReplyOperator:
    def test_is_reply_operator(self):
        assert str(IsReplyOperator()) == "is:reply"

    def test_query_incomplete(self):
        assert isinstance(build(lambda q: q.is_reply()), IncompleteOperator)

    def test_query_build(self):
        assert (
            str(SearchQuery.build(lambda q: q.mention("twitterdev") & q.is_reply()))
            == "@twitterdev is:reply"
        )
