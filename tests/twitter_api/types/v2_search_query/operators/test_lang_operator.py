from twitter_api.types.v2_search_query.operators.lang_operator import LangOperator
from twitter_api.types.v2_search_query.operators.operator import IncompleteOperator
from twitter_api.types.v2_search_query.search_query import SearchQuery, build


class TestLangOperator:
    def test_lang_operator(self):
        assert str(LangOperator("ja")) == "lang:ja"

    def test_query_incomplete(self):
        assert isinstance(build(lambda q: q.lang("ja")), IncompleteOperator)

    def test_query_build(self):
        assert (
            str(SearchQuery.build(lambda q: q.mention("twitterdev") & q.lang("ja")))
            == "@twitterdev lang:ja"
        )
