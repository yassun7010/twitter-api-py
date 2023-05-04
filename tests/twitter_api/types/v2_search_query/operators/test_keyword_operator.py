from twitter_api.types.v2_search_query.operators.keyword_operator import KeywordOperator
from twitter_api.types.v2_search_query.search_query import SearchQuery


class TestKeywordOperator:
    def test_keyword_operator(self):
        assert str(KeywordOperator("test")) == "test"

    def test_keyword_operator_with_phrase(self):
        assert str(KeywordOperator("test twitter")) == '"test twitter"'

    def test_keyword_operator_with_emoji(self):
        assert str(KeywordOperator("😃")) == "😃"

    def test_keyword_operator_with_exact_phrase_match(self):
        assert str(KeywordOperator('"test" twitter')) == r'"\"test\" twitter"'

    def test_query_build(self):
        assert str(SearchQuery.build(lambda q: q.keyword("test"))) == "test"
