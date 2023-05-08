from twitter_api.types.v2_search_query.operators.entity_operator import EntityOperator
from twitter_api.types.v2_search_query.operators.operator import CompleteOperator
from twitter_api.types.v2_search_query.search_query import SearchQuery, build


class TestEntityOperator:
    def test_entity_operator(self):
        assert str(EntityOperator("Michael Jordan")) == 'entity:"Michael Jordan"'

    def test_query_complete(self):
        assert isinstance(
            build(lambda q: q.entity("Michael Jordan")),
            CompleteOperator,
        )

    def test_query_build(self):
        assert (
            str(SearchQuery.build(lambda q: q.entity("Michael Jordan")))
            == 'entity:"Michael Jordan"'
        )
