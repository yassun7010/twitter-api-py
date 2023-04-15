import pytest

from tests.data import json_test_data
from tests.types.convinient_tweets_search_response_body import (
    ConvinientTweetsSearchResponseBody,
)
from twitter_api.api.resources.v2_tweets_search_recent.get_v2_tweets_search_recent import (
    GetV2TweetsSearchRecentResponseBody,
)


@pytest.fixture
def all_fields_response() -> ConvinientTweetsSearchResponseBody:
    return ConvinientTweetsSearchResponseBody.parse_obj(
        GetV2TweetsSearchRecentResponseBody.parse_file(
            json_test_data("get_v2_tweets_search_recent_response_all_fields.json"),
        )
    )


class TestConvinientTweetsSearchResponseBody:
    def test_get_retweeted_tweet(
        self,
        all_fields_response: ConvinientTweetsSearchResponseBody,
    ):
        retweet = all_fields_response.find_tweet("1647123314605965312")
        assert retweet is not None

        retweeted_tweet = all_fields_response.retweeted_by(retweet)

        assert retweeted_tweet is not None
        assert retweeted_tweet.id == "1647031756388962305"

    @pytest.mark.skip("同じレスポンスの中に引用元のツイートが存在しない。")
    def test_get_quoted_tweet(
        self,
        all_fields_response: ConvinientTweetsSearchResponseBody,
    ):
        quote_tweet = all_fields_response.find_tweet("1647031756388962305")
        assert quote_tweet is not None

        quoted_tweet = all_fields_response.quoted_by(quote_tweet)

        assert quoted_tweet is None

    def test_get_replied_tweet(
        self,
        all_fields_response: ConvinientTweetsSearchResponseBody,
    ):
        reply_tweet = all_fields_response.find_tweet("1647123304380268545")
        assert reply_tweet is not None

        replied_tweet = all_fields_response.replied_by(reply_tweet)

        assert replied_tweet is not None
        assert replied_tweet.id == "1647122898220621824"
