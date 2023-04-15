import re

import pytest

from tests.data import json_test_data
from tests.types.convinient_tweet import ConvinientTweetDetail
from twitter_api.api.resources.v2_tweet.get_v2_tweet import GetV2TweetResponseBody


@pytest.fixture
def all_fields_tweet() -> ConvinientTweetDetail:
    return ConvinientTweetDetail.parse_obj(
        GetV2TweetResponseBody.parse_file(
            json_test_data("get_v2_tweet_response_all_fields.json"),
        ).data
    )


class TestConvinientTweetDetail:
    def test_has_tweet_text(self, all_fields_tweet: ConvinientTweetDetail):
        assert len(all_fields_tweet.text) > 0

    def test_has_url(self, all_fields_tweet: ConvinientTweetDetail):
        url_regex = re.compile(r"^https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+")

        assert len(all_fields_tweet.entities_urls) != 0

        for url in all_fields_tweet.entities_urls:
            assert url_regex.match(str(url.expanded_url))

    def test_has_like_count(self, all_fields_tweet: ConvinientTweetDetail):
        assert all_fields_tweet.like_count is not None
