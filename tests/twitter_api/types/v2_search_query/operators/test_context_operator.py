import pytest

from twitter_api.types.v2_domain import Domain
from twitter_api.types.v2_entity.entity import Entity
from twitter_api.types.v2_search_query.operators.context_operator import ContextOperator
from twitter_api.types.v2_search_query.operators.operator import CompleteOperator
from twitter_api.types.v2_search_query.search_query import SearchQuery, build
from twitter_api.types.v2_tweet.tweet_context_annotation import TweetContextAnnotation


@pytest.fixture
def context() -> TweetContextAnnotation:
    return TweetContextAnnotation(
        domain=Domain(
            id="119",
            name="Holiday",
            description="Holidays like Christmas or Halloween",
        ),
        entity=Entity(id="1186637514896920576", name=" New Years Eve"),
    )


class TestContextOperator:
    def test_context_operator(self, context: TweetContextAnnotation):
        assert str(ContextOperator(context)) == "context:119.1186637514896920576"

    def test_context_operator_from_ids(self):
        assert (
            str(ContextOperator(domain_id="10", entity_id="799022225751871488"))
            == "context:10.799022225751871488"
        )

    def test_query_complete(self, context: TweetContextAnnotation):
        assert isinstance(
            build(lambda q: q.context(context)),
            CompleteOperator,
        )

    def test_query_build(self, context: TweetContextAnnotation):
        assert (
            str(SearchQuery.build(lambda q: q.context(context)))
            == "context:119.1186637514896920576"
        )

    def test_query_build_from_ids(self):
        assert (
            str(
                SearchQuery.build(
                    lambda q: q.context(domain_id="10", entity_id="799022225751871488")
                )
            )
            == "context:10.799022225751871488"
        )
