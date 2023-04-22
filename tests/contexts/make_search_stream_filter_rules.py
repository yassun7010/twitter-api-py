from contextlib import contextmanager

from twitter_api.api.resources.v2_tweets_search_stream_rules.post_v2_tweets_search_stream_rules import (
    AddData,
)
from twitter_api.client.twitter_api_client import TwitterApiClient


@contextmanager
def make_search_stream_filter_rules(
    client: TwitterApiClient,
    filters: list[AddData],
):
    """
    ツイート検索のフィルタリングをするためのルールを追加する。
    """

    added_rules = (
        client.chain()
        .resource("https://api.twitter.com/2/tweets/search/stream/rules")
        .post(
            {"add": filters},
        )
    ).data

    yield

    (
        client.chain()
        .resource("https://api.twitter.com/2/tweets/search/stream/rules")
        .post(
            {
                "delete": {
                    "ids": list(map(lambda rule: rule.id, added_rules)),
                },
            }
        )
    )
