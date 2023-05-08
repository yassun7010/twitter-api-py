from twitter_api.types.v2_search_query.operators.list_operator import ListOperator
from twitter_api.types.v2_search_query.operators.operator import CompleteOperator
from twitter_api.types.v2_search_query.search_query import SearchQuery, build


class TestListOperator:
    def test_list_operator(self):
        assert str(ListOperator("123")) == "list:123"

    def test_query_complete(self):
        assert isinstance(
            build(lambda q: q.list("123")),
            CompleteOperator,
        )

    def test_query_build(self):
        assert str(SearchQuery.build(lambda q: q.list("123"))) == "list:123"
