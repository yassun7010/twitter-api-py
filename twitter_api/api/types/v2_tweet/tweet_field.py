from typing import Literal

TweetField = Literal[
    "attachments",
    "author_id",
    "context_annotations",
    "conversation_id",
    "created_at",
    "edit_controls",
    "entities",
    "geo",
    "id",
    "in_reply_to_user_id",
    "lang",
    "non_public_metrics",
    "public_metrics",
    "organic_metrics",
    "promoted_metrics",
    "possibly_sensitive",
    "referenced_tweets",
    "reply_settings",
    "source",
    "text",
    "withheld",
]

ALL_TWEET_FIELDS: list[TweetField] = [
    "attachments",
    "author_id",
    "context_annotations",
    "conversation_id",
    "created_at",
    "edit_controls",
    "entities",
    "geo",
    "id",
    "in_reply_to_user_id",
    "lang",
    "non_public_metrics",
    "public_metrics",
    "organic_metrics",
    "promoted_metrics",
    "possibly_sensitive",
    "referenced_tweets",
    "reply_settings",
    "source",
    "text",
    "withheld",
]
"""
この定数は非公開のフィールドにもアクセスしようとするため、
特別な権限を持ったアカウントでしか使えない。

一般に公開されている情報をすべて取得したい場合、代わりに ALL_PUBLIC_TWEET_FIELDS を使うこと。
"""

ALL_PUBLIC_TWEET_FIELDS: list[TweetField] = [
    "attachments",
    "author_id",
    "context_annotations",
    "conversation_id",
    "created_at",
    "edit_controls",
    "entities",
    "geo",
    "id",
    "in_reply_to_user_id",
    "lang",
    # "non_public_metrics",
    # "organic_metrics",
    "possibly_sensitive",
    # "promoted_metrics",
    "public_metrics",
    "referenced_tweets",
    "reply_settings",
    "source",
    "text",
    "withheld",
]
"""
Tweet の公開されていないメトリクスを読み取るためには、特別な権限が必要になる。

そのため、公開されている情報をすべて取得できるように専用の定数を用意した。
"""
