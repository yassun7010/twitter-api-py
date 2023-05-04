from twitter_api.types.v2_search_query.operators.lang_operator import LangOperator
from twitter_api.types.v2_search_query.search_query import SearchQuery


class TestLangOperator:
    def test_lang_operator(self):
        assert str(LangOperator("ja")) == "lang:ja"

    def test_query_build(self):
        assert (
            str(SearchQuery.build(lambda q: q.mention("twitterdev") & q.lang("ja")))
            == "@twitterdev lang:ja"
        )
