from twitter_api.types.v2_search_query.conversation_id_operator import (
    ConversationIdOperator,
)
from twitter_api.types.v2_search_query.search_query import SearchQuery


class TestConversationId:
    def test_conversation_id(self):
        assert (
            str(ConversationIdOperator("1334987486343299072"))
            == "conversation_id:1334987486343299072"
        )

    def test_query_build(self):
        assert (
            str(SearchQuery.build(lambda q: q.conversation_id("1334987486343299072")))
            == "conversation_id:1334987486343299072"
        )
