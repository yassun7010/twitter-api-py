from typing import Literal, TypeAlias

TweetExpansion: TypeAlias = Literal[
    "attachments.poll_ids",
    "attachments.media_keys",
    "author_id",
    "edit_history_tweet_ids",
    "entities.mentions.username",
    "geo.place_id",
    "in_reply_to_user_id",
    "referenced_tweets.id",
    "referenced_tweets.id.author_id",
]

ALL_TWEET_EXPANSIONS: list[TweetExpansion] = [
    "attachments.poll_ids",
    "attachments.media_keys",
    "author_id",
    "edit_history_tweet_ids",
    "entities.mentions.username",
    "geo.place_id",
    "in_reply_to_user_id",
    "referenced_tweets.id",
    "referenced_tweets.id.author_id",
]
