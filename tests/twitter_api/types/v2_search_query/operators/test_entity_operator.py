from twitter_api.types.v2_search_query.operators.entity_operator import EntityOperator
from twitter_api.types.v2_search_query.search_query import SearchQuery


class TestEntity:
    def test_entity(self):
        assert str(EntityOperator("Michael Jordan")) == 'entity:"Michael Jordan"'

    def test_query_build(self):
        assert (
            str(SearchQuery.build(lambda q: q.entity("Michael Jordan")))
            == 'entity:"Michael Jordan"'
        )
