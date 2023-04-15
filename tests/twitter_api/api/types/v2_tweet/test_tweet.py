import re

import pytest

from tests.data import json_test_data
from twitter_api.api.resources.v2_tweet.get_v2_tweet import GetV2TweetResponseBody
from twitter_api.api.types.v2_tweet.tweet import Tweet


@pytest.fixture
def all_fields_tweet() -> Tweet:
    return Tweet.parse_obj(
        GetV2TweetResponseBody.parse_file(
            json_test_data("get_v2_tweet_response_all_fields.json"),
        ).data
    )


@pytest.fixture
def mention_tweet() -> Tweet:
    return Tweet.parse_file(
        json_test_data("mention_tweet.json"),
    )


class TestTweet:
    def test_has_tweet_text(self, all_fields_tweet: Tweet):
        assert len(all_fields_tweet.text) > 0

    def test_has_urls(self, all_fields_tweet: Tweet):
        url_regex = re.compile(r"^https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+")

        assert len(all_fields_tweet.entities_urls) != 0

        for url in all_fields_tweet.entities_urls:
            assert url_regex.match(str(url.expanded_url))

    def test_has_like_count(self, all_fields_tweet: Tweet):
        assert all_fields_tweet.like_count is not None

    def test_has_mensions(self, mention_tweet: Tweet):
        assert len(mention_tweet.entities_mentions) != 0
