from twitter_api.types.v2_search_query.operators.has_video_link_operator import (
    HasVideoLinkOperator,
)
from twitter_api.types.v2_search_query.operators.operator import IncompleteOperator
from twitter_api.types.v2_search_query.search_query import SearchQuery, build


class TestHasVideoLinkOperator:
    def test_has_video_link_operator(self):
        assert str(HasVideoLinkOperator()) == "has:video_link"

    def test_query_incomplete(self):
        assert isinstance(build(lambda q: q.has_video_link()), IncompleteOperator)

    def test_query_build(self):
        assert (
            str(
                SearchQuery.build(
                    lambda q: q.mention("twitterdev") & q.has_video_link()
                )
            )
            == "@twitterdev has:video_link"
        )
