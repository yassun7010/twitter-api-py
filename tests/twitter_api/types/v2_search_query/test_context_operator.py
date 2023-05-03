from twitter_api.types.v2_search_query.context_operator import ContextOperator
from twitter_api.types.v2_search_query.search_query import SearchQuery


class TestContext:
    def test_context(self):
        assert (
            str(ContextOperator("10.799022225751871488"))
            == "context:10.799022225751871488"
        )

    def test_context_by_ids(self):
        assert (
            str(ContextOperator(domain_id="10", entity_id="799022225751871488"))
            == "context:10.799022225751871488"
        )

    def test_query_build(self):
        assert (
            str(SearchQuery.build(lambda q: q.context("1539382664746020864")))
            == "context:1539382664746020864"
        )
